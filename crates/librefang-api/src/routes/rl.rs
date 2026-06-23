use axum::{routing::post, Json, Router};
use librefang_rl_export::preference::PreferencePair;
use std::sync::Arc;
use crate::routes::AppState;
use crate::types::JsonObject;

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
    axum::extract::State(_state): axum::extract::State<Arc<AppState>>,
    Json(payload): Json<PreferencePair>,
) -> Result<Json<JsonObject>, crate::types::ApiErrorResponse> {
    tracing::info!("Received preference pair: {:?}", payload);
    // Future work: store it via a PreferenceStore in AppState
    Ok(Json(JsonObject(serde_json::json!({ "status": "ok" }))))
}
