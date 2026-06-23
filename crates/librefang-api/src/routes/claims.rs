use crate::routes::AppState;
use axum::{extract::State, http::StatusCode, response::IntoResponse, Json};
use serde::Deserialize;
use std::sync::Arc;

pub fn router() -> axum::Router<Arc<AppState>> {
    axum::Router::new().route("/claims/dedup", axum::routing::post(claim_dedup))
}

#[derive(Deserialize, utoipa::ToSchema)]
pub struct ClaimDedupRequest {
    pub text: String,
}

#[utoipa::path(
    post,
    path = "/api/claims/dedup",
    tag = "claims",
    request_body = ClaimDedupRequest,
    responses((status = 200, description = "Dedup match result", body = crate::types::JsonObject))
)]
pub async fn claim_dedup(
    State(state): State<Arc<AppState>>,
    Json(body): Json<ClaimDedupRequest>,
) -> impl IntoResponse {
    let store = match state.kernel.proactive_memory_store().cloned() {
        Some(s) => s,
        None => {
            return (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({"error": "Proactive memory disabled"})),
            )
        }
    };

    let limit = 5;
    let guard = librefang_memory::namespace_acl::MemoryNamespaceGuard::new(
        librefang_types::user_policy::UserMemoryAccess {
            readable_namespaces: vec!["proactive".into()],
            writable_namespaces: vec![],
            pii_access: false,
            export_allowed: false,
            delete_allowed: false,
        },
    );

    // Using search_all_with_guard from proactive.rs
    let items = match store.search_all_with_guard(&body.text, limit, &guard).await {
        Ok(items) => items,
        Err(_) => {
            return (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({"error": "Search failed"})),
            )
        }
    };

    for item in items {
        if item.category.as_deref() == Some("disinfo_verdict") {
            // Note: Since search_all_with_guard sorts by cosine similarity but drops the exact score
            // we return the top matching semantic item in the verdict category.
            return (
                StatusCode::OK,
                Json(serde_json::json!({"match": true, "verdict": item})),
            );
        }
    }

    (StatusCode::OK, Json(serde_json::json!({"match": false})))
}
