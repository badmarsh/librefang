use crate::routes::AppState;
use axum::{
    extract::{State, WebSocketUpgrade, ws::{WebSocket, Message}},
    response::IntoResponse,
};
use std::sync::Arc;
use tokio_stream::StreamExt;

pub fn router() -> axum::Router<Arc<AppState>> {
    axum::Router::new().route("/desolator/monitor", axum::routing::get(ws_handler))
}

#[utoipa::path(get, path = "/api/desolator/monitor", tag = "desolator", responses((status = 200, description = "WebSocket connection for Media Desolator status")))]
pub async fn ws_handler(
    ws: WebSocketUpgrade,
    State(state): State<Arc<AppState>>,
) -> impl IntoResponse {
    ws.on_upgrade(move |socket| handle_socket(socket, state))
}

async fn handle_socket(mut socket: WebSocket, state: Arc<AppState>) {
    // Subscribe to all kernel events
    let mut rx = state.kernel.event_bus().subscribe_all();
    let mut shutdown_rx = state.kernel.supervisor_ref().subscribe();

    loop {
        tokio::select! {
            event = rx.recv() => {
                match event {
                    Ok(evt) => {
                        // Serialize event via serde
                        let json_evt = serde_json::to_string(&*evt).unwrap_or_else(|_| "{}".to_string());
                        
                        if socket.send(Message::Text(json_evt)).await.is_err() {
                            break; // Client disconnected
                        }
                    }
                    Err(tokio::sync::broadcast::error::RecvError::Lagged(_)) => {
                        continue;
                    }
                    Err(_) => {
                        break;
                    }
                }
            }
            _ = shutdown_rx.changed() => {
                if *shutdown_rx.borrow() {
                    let _ = socket.send(Message::Close(None)).await;
                    break;
                }
            }
            msg = socket.recv() => {
                if msg.is_none() {
                    break; // Client disconnected
                }
            }
        }
    }
}
