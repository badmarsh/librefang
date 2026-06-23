use librefang_rl_export::preference::{PreferencePair, PreferenceStore};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;

pub struct SqlitePreferenceStore {
    pool: Pool<SqliteConnectionManager>,
}

impl SqlitePreferenceStore {
    pub fn new(pool: Pool<SqliteConnectionManager>) -> Self {
        let conn = pool.get().expect("Failed to get db connection");
        conn.execute(
            "CREATE TABLE IF NOT EXISTS rl_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                chosen TEXT NOT NULL,
                rejected TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )",
            [],
        )
        .expect("Failed to create rl_preferences table");

        Self { pool }
    }
}

#[async_trait::async_trait]
impl PreferenceStore for SqlitePreferenceStore {
    async fn store_preference(
        &self,
        pair: PreferencePair,
    ) -> Result<(), librefang_rl_export::ExportError> {
        let pool = self.pool.clone();
        tokio::task::spawn_blocking(move || {
            let conn = pool
                .get()
                .map_err(|e| librefang_rl_export::ExportError::InvalidConfig(e.to_string()))?;
            conn.execute(
                "INSERT INTO rl_preferences (prompt, chosen, rejected) VALUES (?1, ?2, ?3)",
                rusqlite::params![pair.prompt, pair.chosen, pair.rejected],
            )
            .map_err(|e| librefang_rl_export::ExportError::InvalidConfig(e.to_string()))?;
            Ok(())
        })
        .await
        .map_err(|e| librefang_rl_export::ExportError::InvalidConfig(e.to_string()))?
    }
}
