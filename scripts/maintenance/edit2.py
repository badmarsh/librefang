import sys

with open("crates/librefang-wire/src/peer.rs", "r") as f:
    code = f.read()

# Fix 1: Remove `KeyInit` from global scope to fix E0034
code = code.replace("use aes_gcm::{aead::{Aead, KeyInit}, Aes256Gcm, Nonce};", "use aes_gcm::{aead::Aead, Aes256Gcm, Nonce};")

# Add aes_gcm::KeyInit::new_from_slice in the two new functions
code = code.replace("Aes256Gcm::new_from_slice(&key_bytes)", "aes_gcm::KeyInit::new_from_slice(&key_bytes)")


# Fix 2: Tuple return for `sess_key` in `connect_to_peer`
code = code.replace("let sess_key = match &response.kind {", "let (sess_key, use_encryption) = match &response.kind {")
code = code.replace("""                self.registry.add_peer(PeerEntry {
                    node_id: node_id.clone(),
                    node_name: node_name.clone(),
                    address: addr,
                    agents: agents.clone(),
                    state: PeerState::Connected,
                    connected_at: chrono::Utc::now(),
                    protocol_version: *protocol_version,
                });
                key
            }""", """                self.registry.add_peer(PeerEntry {
                    node_id: node_id.clone(),
                    node_name: node_name.clone(),
                    address: addr,
                    agents: agents.clone(),
                    state: PeerState::Connected,
                    connected_at: chrono::Utc::now(),
                    protocol_version: *protocol_version,
                });
                (key, use_encryption)
            }""")


# Fix 3: Tuple return for `session_key` in `send_to_peer`
code = code.replace("let mut use_encryption = false;\n        let session_key = match &ack.kind {", "let (session_key, use_encryption) = match &ack.kind {")
code = code.replace("""                match ack_eph {
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
            }""", """                let mut use_encryption = false;
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
                }
                (key, use_encryption)
            }""")


# Fix 4: Tuple return for `start_with_identity` accept loop
code = code.replace("let (peer_node_id, session_key) = match &msg.kind {", "let (peer_node_id, session_key, use_encryption) = match &msg.kind {")

code = code.replace("""                // Register the peer
                registry.add_peer(PeerEntry {
                    node_id: node_id.clone(),
                    node_name: node_name.clone(),
                    address: addr,
                    agents: agents.clone(),
                    state: PeerState::Connected,
                    connected_at: chrono::Utc::now(),
                    protocol_version: *protocol_version,
                });

                (node_id.clone(), session_key)
            }""", """                // Register the peer
                registry.add_peer(PeerEntry {
                    node_id: node_id.clone(),
                    node_name: node_name.clone(),
                    address: addr,
                    agents: agents.clone(),
                    state: PeerState::Connected,
                    connected_at: chrono::Utc::now(),
                    protocol_version: *protocol_version,
                });

                (node_id.clone(), session_key, use_encryption)
            }""")


with open("crates/librefang-wire/src/peer.rs", "w") as f:
    f.write(code)
