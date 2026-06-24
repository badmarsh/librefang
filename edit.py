import sys
import re

with open("scratch_peer.rs", "r") as f:
    code = f.read()

# 1. Imports
imports = """
use aes_gcm::{aead::{Aead, KeyInit}, Aes256Gcm, Nonce};
use rand_core::{OsRng, RngCore};
"""
code = code.replace("use sha2::Sha256;\n", "use sha2::Sha256;\n" + imports)

# 2. Add write_message_encrypted and read_message_encrypted_observed after write_message_authenticated
new_funcs = """
/// SECURITY: Write an AES-256-GCM encrypted framed message.
pub async fn write_message_encrypted(
    writer: &mut tokio::net::tcp::OwnedWriteHalf,
    msg: &WireMessage,
    session_key: &str,
) -> Result<(), WireError> {
    let json_bytes = serde_json::to_vec(msg)?;
    
    let key_bytes = hex::decode(session_key)
        .map_err(|_| WireError::HandshakeFailed("Invalid session key hex".into()))?;
    if key_bytes.len() != 32 {
        return Err(WireError::HandshakeFailed("Session key must be 32 bytes for AES-256".into()));
    }
    
    let cipher = Aes256Gcm::new_from_slice(&key_bytes).map_err(|_| WireError::HandshakeFailed("Invalid key length".into()))?;
    
    let mut nonce_bytes = [0u8; 12];
    OsRng.fill_bytes(&mut nonce_bytes);
    let nonce = Nonce::from_slice(&nonce_bytes);
    
    let encrypted = cipher.encrypt(nonce, json_bytes.as_ref())
        .map_err(|_| WireError::HandshakeFailed("Encryption failed".into()))?;
        
    let total_len = nonce_bytes.len() + encrypted.len();
    let len_bytes = (total_len as u32).to_be_bytes();
    
    writer.write_all(&len_bytes).await?;
    writer.write_all(&nonce_bytes).await?;
    writer.write_all(&encrypted).await?;
    writer.flush().await?;
    Ok(())
}

/// SECURITY: Read an AES-256-GCM encrypted framed message.
pub async fn read_message_encrypted_observed(
    reader: &mut tokio::net::tcp::OwnedReadHalf,
    session_key: &str,
    peer_node_id: &str,
) -> Result<WireMessage, WireError> {
    let mut header = [0u8; 4];
    match reader.read_exact(&mut header).await {
        Ok(_) => {}
        Err(e) if e.kind() == std::io::ErrorKind::UnexpectedEof => {
            return Err(WireError::ConnectionClosed);
        }
        Err(e) => return Err(WireError::Io(e)),
    }

    let len = decode_length(&header);
    if len > MAX_MESSAGE_SIZE {
        return Err(WireError::MessageTooLarge {
            size: len,
            max: MAX_MESSAGE_SIZE,
        });
    }

    if len < 12 + 16 + 2 {
        return Err(WireError::HandshakeFailed("Message too short for encrypted frame".into()));
    }

    let mut frame = vec![0u8; len as usize];
    reader.read_exact(&mut frame).await?;

    let nonce_bytes = &frame[..12];
    let encrypted = &frame[12..];

    let key_bytes = hex::decode(session_key)
        .map_err(|_| WireError::HandshakeFailed("Invalid session key hex".into()))?;
    if key_bytes.len() != 32 {
        return Err(WireError::HandshakeFailed("Session key must be 32 bytes for AES-256".into()));
    }
    
    let cipher = Aes256Gcm::new_from_slice(&key_bytes).map_err(|_| WireError::HandshakeFailed("Invalid key length".into()))?;
    let nonce = Nonce::from_slice(nonce_bytes);

    let decrypted = cipher.decrypt(nonce, encrypted)
        .map_err(|_| WireError::HandshakeFailed("AES-GCM decryption/authentication failed".into()))?;

    let msg = decode_message(&decrypted)?;
    if let Some(unk) = classify_unknown(&decrypted, &msg) {
        warn!(
            target: "wire::compat",
            peer = %peer_node_id,
            msg_id = %msg.id,
            level = %unk.level.name(),
            raw_tag = %unk.raw_tag,
            "ignoring unrecognised wire variant from peer"
        );
    }
    Ok(msg)
}

pub async fn read_message_encrypted_pre_handshake(
    reader: &mut tokio::net::tcp::OwnedReadHalf,
    session_key: &str,
) -> Result<WireMessage, WireError> {
    read_message_encrypted_observed(reader, session_key, "<pre-handshake>").await
}
"""

code = code.replace("pub async fn read_message(\n", new_funcs + "\npub async fn read_message(\n")


# 3. Update connect_to_peer
old_1 = """                let key = match ack_eph {
                    Some(remote_eph) => {
                        let transcript = crate::kex::handshake_transcript(&our_nonce, ack_nonce);
                        our_kex
                            .derive_session_key(remote_eph, &transcript)
                            .map_err(|e| {
                                WireError::HandshakeFailed(format!("X25519 ECDH failed: {e}"))
                            })?
                    }
                    None => derive_session_key(&self.config.shared_secret, &our_nonce, ack_nonce),
                };"""
new_1 = """                let mut use_encryption = false;
                let key = match ack_eph {
                    Some(remote_eph) => {
                        let transcript = crate::kex::handshake_transcript(&our_nonce, ack_nonce);
                        use_encryption = true;
                        our_kex
                            .derive_session_key(remote_eph, &transcript)
                            .map_err(|e| {
                                WireError::HandshakeFailed(format!("X25519 ECDH failed: {e}"))
                            })?
                    }
                    None => {
                        if self.config.frame_encryption == librefang_types::config::FrameEncryptionMode::Required {
                            return Err(WireError::HandshakeFailed("Peer does not support required AES-256-GCM encryption".into()));
                        }
                        derive_session_key(&self.config.shared_secret, &our_nonce, ack_nonce)
                    }
                };
                if self.config.frame_encryption == librefang_types::config::FrameEncryptionMode::Plaintext {
                    use_encryption = false;
                }"""
code = code.replace(old_1, new_1)

code = code.replace("""            if let Err(e) = connection_loop(
                &mut reader,
                &mut writer,
                &peer_node_id,
                &registry,
                &*handle,
                Some(&sess_key),
                &rate_limiter_clone,
            )""", """            if let Err(e) = connection_loop(
                &mut reader,
                &mut writer,
                &peer_node_id,
                &registry,
                &*handle,
                Some(&sess_key),
                use_encryption,
                &rate_limiter_clone,
            )""")


# 4. Update send_to_peer
old_2 = """        let session_key = match &ack.kind {
            WireMessageKind::Response(WireResponse::HandshakeAck {
                node_id: ack_node_id,
                nonce: ack_nonce,
                auth_hmac: ack_hmac,
                protocol_version,
                public_key: ack_pubkey,
                identity_signature: ack_identity_sig,
                ephemeral_pubkey: ack_eph,
                ..
            }) => {
                if *protocol_version != PROTOCOL_VERSION {
                    return Err(WireError::VersionMismatch {
                        local: PROTOCOL_VERSION,
                        remote: *protocol_version,
                    });
                }
                // SECURITY (#3875): Verify ack HMAC — includes our own node_id
                // as recipient so the ack is bound to this node specifically.
                let expected_ack_data =
                    format!("{}|{}|{}", ack_nonce, ack_node_id, self.config.node_id);
                if !hmac_verify(
                    &self.config.shared_secret,
                    expected_ack_data.as_bytes(),
                    ack_hmac,
                ) {
                    return Err(WireError::HandshakeFailed(
                        "HMAC verification of HandshakeAck failed".to_string(),
                    ));
                }

                // SECURITY (#3873): Verify identity
                if let (Some(pk), Some(sig)) = (ack_pubkey, ack_identity_sig) {
                    self.verify_peer_identity(ack_node_id, expected_ack_data.as_bytes(), pk, sig, ack_eph.as_deref())?;
                } else {
                    // No identity provided -> legacy TOFU fallback (reject if we have a pin)
                    self.enforce_tofu_pin(ack_node_id, None)?;
                }

                // SECURITY (#4269): Prefer ECDH-derived session_key
                match ack_eph {
                    Some(remote_eph) => {
                        let transcript = crate::kex::handshake_transcript(&our_nonce, ack_nonce);
                        our_kex
                            .derive_session_key(remote_eph, &transcript)
                            .map_err(|e| {
                                WireError::HandshakeFailed(format!("X25519 ECDH failed: {e}"))
                            })?
                    }
                    None => derive_session_key(&self.config.shared_secret, &our_nonce, ack_nonce),
                }
            }"""
            
new_2 = """        let mut use_encryption = false;
        let session_key = match &ack.kind {
            WireMessageKind::Response(WireResponse::HandshakeAck {
                node_id: ack_node_id,
                nonce: ack_nonce,
                auth_hmac: ack_hmac,
                protocol_version,
                public_key: ack_pubkey,
                identity_signature: ack_identity_sig,
                ephemeral_pubkey: ack_eph,
                ..
            }) => {
                if *protocol_version != PROTOCOL_VERSION {
                    return Err(WireError::VersionMismatch {
                        local: PROTOCOL_VERSION,
                        remote: *protocol_version,
                    });
                }
                let expected_ack_data =
                    format!("{}|{}|{}", ack_nonce, ack_node_id, self.config.node_id);
                if !hmac_verify(
                    &self.config.shared_secret,
                    expected_ack_data.as_bytes(),
                    ack_hmac,
                ) {
                    return Err(WireError::HandshakeFailed(
                        "HMAC verification of HandshakeAck failed".to_string(),
                    ));
                }
                if let (Some(pk), Some(sig)) = (ack_pubkey, ack_identity_sig) {
                    self.verify_peer_identity(ack_node_id, expected_ack_data.as_bytes(), pk, sig, ack_eph.as_deref())?;
                } else {
                    self.enforce_tofu_pin(ack_node_id, None)?;
                }

                match ack_eph {
                    Some(remote_eph) => {
                        let transcript = crate::kex::handshake_transcript(&our_nonce, ack_nonce);
                        use_encryption = true;
                        our_kex
                            .derive_session_key(remote_eph, &transcript)
                            .map_err(|e| {
                                WireError::HandshakeFailed(format!("X25519 ECDH failed: {e}"))
                            })?
                    }
                    None => {
                        if self.config.frame_encryption == librefang_types::config::FrameEncryptionMode::Required {
                            return Err(WireError::HandshakeFailed("Peer does not support required AES-256-GCM encryption".into()));
                        }
                        derive_session_key(&self.config.shared_secret, &our_nonce, ack_nonce)
                    }
                }
            }"""
code = code.replace(old_2, new_2)

old_2b = """
        if self.config.frame_encryption == librefang_types::config::FrameEncryptionMode::Plaintext {
            use_encryption = false;
        }

        let msg = WireMessage {
            id: uuid::Uuid::new_v4().to_string(),
            kind: WireMessageKind::Request(WireRequest::AgentMessage {
                agent: agent.to_string(),
                message: message.to_string(),
                sender: sender.map(|s| s.to_string()),
            }),
        };
        write_message_authenticated(&mut writer, &msg, &session_key).await?;

        // Wait for response
        let resp = read_message_authenticated(&mut reader, &session_key).await?;
"""

code = code.replace("""        let msg = WireMessage {
            id: uuid::Uuid::new_v4().to_string(),
            kind: WireMessageKind::Request(WireRequest::AgentMessage {
                agent: agent.to_string(),
                message: message.to_string(),
                sender: sender.map(|s| s.to_string()),
            }),
        };
        write_message_authenticated(&mut writer, &msg, &session_key).await?;

        // Wait for response
        let resp = read_message_authenticated(&mut reader, &session_key).await?;""", """        if self.config.frame_encryption == librefang_types::config::FrameEncryptionMode::Plaintext {
            use_encryption = false;
        }

        let msg = WireMessage {
            id: uuid::Uuid::new_v4().to_string(),
            kind: WireMessageKind::Request(WireRequest::AgentMessage {
                agent: agent.to_string(),
                message: message.to_string(),
                sender: sender.map(|s| s.to_string()),
            }),
        };
        
        if use_encryption {
            write_message_encrypted(&mut writer, &msg, &session_key).await?;
        } else {
            write_message_authenticated(&mut writer, &msg, &session_key).await?;
        }

        let resp = if use_encryption {
            read_message_encrypted_pre_handshake(&mut reader, &session_key).await?
        } else {
            read_message_authenticated(&mut reader, &session_key).await?
        };""")


# 5. Update start_with_identity loop
old_3 = """                // SECURITY (#4269): Prefer ECDH-derived session_key when the
                // KEX was completed on both sides; legacy fallback otherwise.
                let session_key = match (our_kex, peer_eph.as_deref()) {
                    (Some(kex), Some(remote_eph)) => {
                        let transcript = crate::kex::handshake_transcript(nonce, &ack_nonce);
                        kex.derive_session_key(remote_eph, &transcript)
                            .map_err(|e| {
                                WireError::HandshakeFailed(format!("X25519 ECDH failed: {e}"))
                            })?
                    }
                    _ => derive_session_key(&node.config.shared_secret, nonce, &ack_nonce),
                };"""
new_3 = """                let mut use_encryption = false;
                let session_key = match (our_kex, peer_eph.as_deref()) {
                    (Some(kex), Some(remote_eph)) => {
                        let transcript = crate::kex::handshake_transcript(nonce, &ack_nonce);
                        use_encryption = true;
                        kex.derive_session_key(remote_eph, &transcript)
                            .map_err(|e| {
                                WireError::HandshakeFailed(format!("X25519 ECDH failed: {e}"))
                            })?
                    }
                    _ => {
                        if node.config.frame_encryption == librefang_types::config::FrameEncryptionMode::Required {
                            return Err(WireError::HandshakeFailed("Peer does not support required AES-256-GCM encryption".into()));
                        }
                        derive_session_key(&node.config.shared_secret, nonce, &ack_nonce)
                    }
                };
                if node.config.frame_encryption == librefang_types::config::FrameEncryptionMode::Plaintext {
                    use_encryption = false;
                }"""
code = code.replace(old_3, new_3)

code = code.replace("""        if let Err(e) = connection_loop(
            &mut reader,
            &mut writer,
            &peer_node_id,
            registry,
            handle,
            Some(&session_key),
            &node.rate_limiter,
        )""", """        if let Err(e) = connection_loop(
            &mut reader,
            &mut writer,
            &peer_node_id,
            registry,
            handle,
            Some(&session_key),
            use_encryption,
            &node.rate_limiter,
        )""")


# 6. Update connection_loop body
old_4 = """async fn connection_loop(
    reader: &mut tokio::net::tcp::OwnedReadHalf,
    writer: &mut tokio::net::tcp::OwnedWriteHalf,
    peer_node_id: &str,
    registry: &PeerRegistry,
    handle: &dyn PeerHandle,
    session_key: Option<&str>,
    rate_limiter: &PeerRateLimiter,
) -> Result<(), WireError> {
    loop {
        let msg = match if let Some(key) = session_key {
            // Both helpers thread `peer_node_id` so the
            // `wire::compat` warn emitted on Unknown-variant decode
            // is labelled with the actual peer, not the
            // pre-handshake placeholder (audit:
            // wire-message-other-variant-silent).
            read_message_authenticated_observed(reader, key, peer_node_id).await
        } else {
            read_message_observed(reader, peer_node_id).await
        } {"""
new_4 = """async fn connection_loop(
    reader: &mut tokio::net::tcp::OwnedReadHalf,
    writer: &mut tokio::net::tcp::OwnedWriteHalf,
    peer_node_id: &str,
    registry: &PeerRegistry,
    handle: &dyn PeerHandle,
    session_key: Option<&str>,
    use_encryption: bool,
    rate_limiter: &PeerRateLimiter,
) -> Result<(), WireError> {
    loop {
        let msg = match if let Some(key) = session_key {
            if use_encryption {
                read_message_encrypted_observed(reader, key, peer_node_id).await
            } else {
                read_message_authenticated_observed(reader, key, peer_node_id).await
            }
        } else {
            read_message_observed(reader, peer_node_id).await
        } {"""
code = code.replace(old_4, new_4)

old_5 = """                if let Some(key) = session_key {
                    write_message_authenticated(writer, &response, key).await?;
                } else {
                    write_message(writer, &response).await?;
                }"""
new_5 = """                if let Some(key) = session_key {
                    if use_encryption {
                        write_message_encrypted(writer, &response, key).await?;
                    } else {
                        write_message_authenticated(writer, &response, key).await?;
                    }
                } else {
                    write_message(writer, &response).await?;
                }"""
code = code.replace(old_5, new_5)

with open("scratch_peer.rs", "w") as f:
    f.write(code)

