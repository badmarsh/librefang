use agent_client_protocol_schema::{Implementation, InitializeResponse, ProtocolVersion};
use jsonschema::JSONSchema;
use schemars::schema_for;

#[tokio::test]
async fn test_server_responses_match_schema() {
    let schema = schema_for!(InitializeResponse);
    let schema_json = serde_json::to_value(&schema).unwrap();
    let compiled_schema = JSONSchema::compile(&schema_json).expect("A valid schema");

    let mut result = InitializeResponse::new(ProtocolVersion::V1);
    result.agent_info = Some(Implementation::new("librefang-acp", "0.1.0"));

    let response_json = serde_json::to_value(&result).unwrap();
    let validation_result = compiled_schema.validate(&response_json);

    if let Err(errors) = validation_result {
        for error in errors {
            println!("Validation error: {}", error);
        }
        panic!("Response did not match schema");
    }
}
