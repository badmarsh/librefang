import sys
import json
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import pipeline
except ImportError:
    print(json.dumps({"error": "transformers library not installed"}))
    sys.exit(1)

def main():
    try:
        # Load the feature-extraction pipeline using slovakbert
        extractor = pipeline('feature-extraction', model='gerulata/slovakbert')
        
        # Read text from stdin
        input_data = sys.stdin.read().strip()
        if not input_data:
            print(json.dumps({"error": "No input provided"}))
            return
            
        data = json.loads(input_data)
        text = data.get("text", "")
        if not text:
            print(json.dumps({"error": "No text provided"}))
            return
            
        # Replace curly quotes per model recommendations
        text = text.replace("“", '"').replace("”", '"')
        
        # Extract embeddings
        features = extractor(text)
        
        # Take the mean of the embeddings over tokens to get a sentence embedding
        # The output of feature-extraction is usually [1, seq_len, hidden_size]
        if isinstance(features, list) and len(features) > 0:
            seq_embeddings = features[0]
            # Simple mean pooling
            if len(seq_embeddings) > 0:
                hidden_size = len(seq_embeddings[0])
                mean_embedding = [0.0] * hidden_size
                for token_emb in seq_embeddings:
                    for i in range(hidden_size):
                        mean_embedding[i] += token_emb[i]
                mean_embedding = [x / len(seq_embeddings) for x in mean_embedding]
                print(json.dumps({"embedding": mean_embedding}))
                return
                
        print(json.dumps({"error": "Failed to extract embeddings"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
