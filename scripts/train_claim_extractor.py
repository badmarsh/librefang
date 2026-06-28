#!/usr/bin/env python3
import argparse
import os
import sys
import logging
import json
import torch
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def generate_dummy_data():
    """Generates synthetic JSONL data for automated testing and CI/CD."""
    logger.info("Generating dummy data for auto-distillation test...")
    dummy_data = [
        {"text": "Nové predpisy EÚ zakážu hotovosť na Slovensku.", "extracted_claims": ["zakážu hotovosť na Slovensku"]},
        {"text": "Dnes bude pršať.", "extracted_claims": []},
        {"text": "NATO buduje jadrovú základňu v Tatrách.", "extracted_claims": ["NATO buduje jadrovú základňu v Tatrách"]},
        {"text": "Vláda odstúpila po korupčnom škandále.", "extracted_claims": ["Vláda odstúpila"]},
        {"text": "Káva je dobrá.", "extracted_claims": []}
    ] * 20  # Duplicate to make 100 samples
    return dummy_data

def align_labels_with_tokens(word_labels, word_ids):
    new_labels = []
    current_word = None
    for word_id in word_ids:
        if word_id is None:
            new_labels.append(-100)
        elif word_id != current_word:
            new_labels.append(word_labels[word_id])
            current_word = word_id
        else:
            # We assign -100 to subsequent subwords so they are ignored in the loss
            new_labels.append(-100)
    return new_labels

def main():
    parser = argparse.ArgumentParser(description="Auto-Distillation Pipeline for Claim Extractor (Teacher-Student)")
    parser.add_argument("--data", type=str, help="Path to JSONL dataset distilled from Teacher LLM")
    parser.add_argument("--dummy-data", action="store_true", help="Use synthetic data to verify training loop")
    parser.add_argument("--model-name", type=str, default="gerulata/slovakbert", help="Base model for student")
    parser.add_argument("--output-dir", type=str, default="models/slovakbert_claim_extractor", help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs")
    
    args = parser.parse_args()
    
    if not args.data and not args.dummy_data:
        parser.error("Must provide either --data or --dummy-data")
        
    try:
        from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification
        from datasets import Dataset
    except ImportError as e:
        logger.error(f"Missing required libraries (transformers, datasets, torch). Details: {e}")
        sys.exit(1)
        
    if args.dummy_data:
        raw_data = generate_dummy_data()
    else:
        logger.info(f"Loading distilled labels from {args.data}")
        with open(args.data, "r", encoding="utf-8") as f:
            raw_data = [json.loads(line) for line in f]
            
    logger.info("Tokenizing dataset and aligning string labels to BIO tags...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)
    
    # Process dataset
    all_inputs = {"input_ids": [], "attention_mask": [], "labels": []}
    for item in raw_data:
        text = item["text"]
        claims = item.get("extracted_claims", [])
        
        tokenized_inputs = tokenizer(text, truncation=True, max_length=128)
        word_ids = tokenized_inputs.word_ids()
        
        # Determine number of unique words
        num_words = len(set([w for w in word_ids if w is not None]))
        word_labels = [0] * num_words  # Initialize all words as 'O' (0)
        
        for claim in claims:
            start_char = text.find(claim)
            if start_char != -1:
                end_char = start_char + len(claim) - 1
                
                # Find start and end word indices
                start_word = tokenized_inputs.char_to_word(start_char)
                end_word = tokenized_inputs.char_to_word(end_char)
                
                if start_word is not None and end_word is not None:
                    word_labels[start_word] = 1  # B-CLAIM
                    for w in range(start_word + 1, end_word + 1):
                        if w < num_words:
                            word_labels[w] = 2  # I-CLAIM
                            
        labels = align_labels_with_tokens(word_labels, word_ids)
        
        all_inputs["input_ids"].append(tokenized_inputs["input_ids"])
        all_inputs["attention_mask"].append(tokenized_inputs["attention_mask"])
        all_inputs["labels"].append(labels)
        
    dataset = Dataset.from_dict(all_inputs)
    # Split for dummy eval
    dataset = dataset.train_test_split(test_size=0.2)
    
    logger.info(f"Loading Student Model: {args.model_name} (num_labels=3)")
    model = AutoModelForTokenClassification.from_pretrained(args.model_name, num_labels=3)
    
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
    
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=args.epochs,
        weight_decay=0.01,
        save_strategy="epoch",
        disable_tqdm=True
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        processing_class=tokenizer,
        data_collator=data_collator,
    )
    
    logger.info("Starting auto-distillation training loop...")
    trainer.train()
    
    logger.info("Evaluating distilled model...")
    eval_results = trainer.evaluate()
    for k, v in eval_results.items():
        logger.info(f"  {k}: {v:.4f}")
        
    logger.info(f"Saving final distilled student model to {args.output_dir}")
    os.makedirs(args.output_dir, exist_ok=True)
    trainer.save_model(args.output_dir)
    logger.info("Distillation pipeline completed successfully.")

if __name__ == "__main__":
    main()
