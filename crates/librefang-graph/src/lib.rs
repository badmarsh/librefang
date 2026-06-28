pub mod graph;
pub mod centrality;
pub mod community;
pub mod corroboration;
pub mod risk;
pub mod temporal;

use neo4rs::{Graph, query};
use serde::{Deserialize, Serialize};

#[derive(Debug, thiserror::Error)]
pub enum GraphError {
    #[error("Database error: {0}")]
    Database(String),
}

pub struct NetworkMapperGraph {
    graph: Graph,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Actor {
    pub id: String,
    pub name: String,
}

impl NetworkMapperGraph {
    pub async fn new(uri: &str, user: &str, pass: &str) -> Result<Self, GraphError> {
        let graph = Graph::new(uri, user, pass)
            .await
            .map_err(|e| GraphError::Database(e.to_string()))?;
        Ok(Self { graph })
    }

    pub async fn add_actor(&self, actor: &Actor) -> Result<(), GraphError> {
        self.graph.run(query("MERGE (a:Actor {id: $id, name: $name})")
            .param("id", actor.id.clone())
            .param("name", actor.name.clone()))
            .await
            .map_err(|e| GraphError::Database(e.to_string()))?;
        Ok(())
    }
}
