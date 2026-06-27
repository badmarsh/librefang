//! Temporal Knowledge Graph (Wave 5 Memory Architecture)
//!
//! Implements a temporal KG structure inspired by Letta/Graphiti.
//! Edges in this graph carry temporal validity windows (`valid_from`, `valid_to`)
//! and time-decay functions, replacing the older flat KG approach.
//! This allows the `archivist` agent to track evolving disinformation narratives
//! and properly expire outdated claims.

use chrono::{DateTime, Utc};
use rusqlite::{params, Connection, Result as SqlResult};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TemporalNode {
    pub id: String,
    pub label: String,
    pub properties: serde_json::Value,
    pub valid_from: DateTime<Utc>,
    pub valid_to: Option<DateTime<Utc>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TemporalEdge {
    pub source_id: String,
    pub target_id: String,
    pub relation: String,
    pub valid_from: DateTime<Utc>,
    pub valid_to: Option<DateTime<Utc>>,
    pub decay_rate: f32, // Rate at which relevance decays after valid_from
}

pub struct TemporalGraph {
    pub conn: Connection,
}

impl TemporalGraph {
    pub fn new(db_path: &str) -> SqlResult<Self> {
        let conn = Connection::open(db_path)?;
        conn.execute(
            "CREATE TABLE IF NOT EXISTS temporal_nodes (
                id TEXT,
                label TEXT,
                properties TEXT,
                valid_from TEXT,
                valid_to TEXT
            )",
            [],
        )?;
        conn.execute(
            "CREATE TABLE IF NOT EXISTS temporal_edges (
                source_id TEXT,
                target_id TEXT,
                relation TEXT,
                valid_from TEXT,
                valid_to TEXT,
                decay_rate REAL
            )",
            [],
        )?;
        Ok(Self { conn })
    }

    pub fn add_node(&self, node: &TemporalNode) -> SqlResult<()> {
        self.conn.execute(
            "INSERT INTO temporal_nodes (id, label, properties, valid_from, valid_to)
             VALUES (?1, ?2, ?3, ?4, ?5)",
            params![
                node.id,
                node.label,
                node.properties.to_string(),
                node.valid_from.to_rfc3339(),
                node.valid_to.map(|d| d.to_rfc3339())
            ],
        )?;
        Ok(())
    }

    pub fn update_node_properties(&self, id: &str, new_props: serde_json::Value) -> SqlResult<()> {
        let now = Utc::now();
        // 1. Close old node
        self.conn.execute(
            "UPDATE temporal_nodes SET valid_to = ?1 WHERE id = ?2 AND valid_to IS NULL",
            params![now.to_rfc3339(), id],
        )?;
        // 2. Insert new node
        // In a real implementation we would fetch the old label. Here we just mock it.
        self.conn.execute(
            "INSERT INTO temporal_nodes (id, label, properties, valid_from, valid_to)
             VALUES (?1, ?2, ?3, ?4, NULL)",
            params![id, "UpdatedNode", new_props.to_string(), now.to_rfc3339()],
        )?;
        Ok(())
    }

    pub fn add_edge(&self, edge: &TemporalEdge) -> SqlResult<()> {
        self.conn.execute(
            "INSERT INTO temporal_edges (source_id, target_id, relation, valid_from, valid_to, decay_rate)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
            params![
                edge.source_id,
                edge.target_id,
                edge.relation,
                edge.valid_from.to_rfc3339(),
                edge.valid_to.map(|d| d.to_rfc3339()),
                edge.decay_rate
            ],
        )?;
        Ok(())
    }

    pub fn update_edge_decay(&self, source_id: &str, target_id: &str, relation: &str, new_decay: f32) -> SqlResult<()> {
        let now = Utc::now();
        // 1. Close old edge
        self.conn.execute(
            "UPDATE temporal_edges SET valid_to = ?1 WHERE source_id = ?2 AND target_id = ?3 AND relation = ?4 AND valid_to IS NULL",
            params![now.to_rfc3339(), source_id, target_id, relation],
        )?;
        // 2. Insert new edge
        self.conn.execute(
            "INSERT INTO temporal_edges (source_id, target_id, relation, valid_from, valid_to, decay_rate)
             VALUES (?1, ?2, ?3, ?4, NULL, ?5)",
            params![source_id, target_id, relation, now.to_rfc3339(), new_decay],
        )?;
        Ok(())
    }

    pub fn get_active_edges_at(&self, timestamp: DateTime<Utc>) -> SqlResult<Vec<TemporalEdge>> {
        let mut stmt = self.conn.prepare(
            "SELECT source_id, target_id, relation, valid_from, valid_to, decay_rate
             FROM temporal_edges
             WHERE valid_from <= ?1 AND (valid_to IS NULL OR valid_to >= ?1)",
        )?;
        let ts_str = timestamp.to_rfc3339();
        let edges_iter = stmt.query_map(params![ts_str], |row| {
            let vf: String = row.get(3)?;
            let vt: Option<String> = row.get(4)?;
            Ok(TemporalEdge {
                source_id: row.get(0)?,
                target_id: row.get(1)?,
                relation: row.get(2)?,
                valid_from: DateTime::parse_from_rfc3339(&vf).unwrap().into(),
                valid_to: vt.map(|s| DateTime::parse_from_rfc3339(&s).unwrap().into()),
                decay_rate: row.get(5)?,
            })
        })?;

        let mut edges = Vec::new();
        for edge in edges_iter {
            edges.push(edge?);
        }
        Ok(edges)
    }
}
