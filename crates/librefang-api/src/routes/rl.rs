use crate::routes::AppState;
use crate::types::JsonObject;
use axum::{routing::post, Json, Router};
use librefang_rl_export::preference::PreferencePair;
use std::sync::Arc;

pub fn router() -> Router<Arc<AppState>> {
    Router::new().route("/rl/preference", post(submit_preference))
}

#[utoipa::path(
    post,
    path = "/api/v1/rl/preference",
    request_body = JsonObject,
    responses(
        (status = 200, description = "Preference pair submitted successfully", body = JsonObject)
    )
)]
pub async fn submit_preference(
    axum::extract::State(state): axum::extract::State<Arc<AppState>>,
    Json(payload): Json<PreferencePair>,
) -> Result<Json<JsonObject>, crate::types::ApiErrorResponse> {
    tracing::info!("Received preference pair: {:?}", payload);
    if let Some(store) = &state.preference_store {
        store.store_preference(payload).await.map_err(|e| {
            crate::types::ApiErrorResponse::internal(format!("Failed to store preference: {}", e))
        })?;
    } else {
        tracing::warn!("Preference store not configured, dropping preference pair");
    }
    Ok(Json(JsonObject(serde_json::json!({ "status": "ok" }))))
}
