//! Secure TLS transport layer for OFP frames.

use rustls::{ClientConfig, ServerConfig};
use std::sync::Arc;
use tokio::net::TcpStream;
use tokio_rustls::{TlsAcceptor, TlsConnector, client::TlsStream as ClientTlsStream, server::TlsStream as ServerTlsStream};

/// Wrapper around a secure TLS stream for OFP.
pub enum SecureStream {
    Client(ClientTlsStream<TcpStream>),
    Server(ServerTlsStream<TcpStream>),
}

/// Upgrades a plain TCP stream to an mTLS secure stream.
pub async fn upgrade_to_mtls_client(
    stream: TcpStream,
    domain: &str,
    config: Arc<ClientConfig>,
) -> std::io::Result<SecureStream> {
    let connector = TlsConnector::from(config);
    let server_name = rustls::pki_types::ServerName::try_from(domain)
        .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidInput, e))?;
    
    let tls_stream = connector.connect(server_name.to_owned(), stream).await?;
    Ok(SecureStream::Client(tls_stream))
}

pub async fn upgrade_to_mtls_server(
    stream: TcpStream,
    config: Arc<ServerConfig>,
) -> std::io::Result<SecureStream> {
    let acceptor = TlsAcceptor::from(config);
    let tls_stream = acceptor.accept(stream).await?;
    Ok(SecureStream::Server(tls_stream))
}
