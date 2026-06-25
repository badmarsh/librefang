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
    """Generates synthetic BIO-tagged data for automated testing and CI/CD."""
    logger.info("Generating dummy data for auto-distillation test...")
    # Sentences and token labels: 0=O, 1=B-CLAIM, 2=I-CLAIM
    dummy_data = [
        {"tokens": ["Nové", "predpisy", "EÚ", "zakážu", "hotovosť", "na", "Slovensku", "."],
         "labels": [0, 0, 0, 1, 2, 2, 2, 0]},
        {"tokens": ["Dnes", "bude", "pršať", "."], 
         "labels": [0, 0, 0, 0]},
        {"tokens": ["NATO", "buduje", "jadrovú", "základňu", "v", "Tatrách", "."],
         "labels": [1, 2, 2, 2, 2, 2, 0]},
        {"tokens": ["Vláda", "odstúpila", "po", "korupčnom", "škandále", "."],
         "labels": [1, 2, 2, 2, 2, 0]},
        {"tokens": ["Káva", "je", "dobrá", "."], 
         "labels": [0, 0, 0, 0]}
    ] * 20  # Duplicate to make 100 samples
    return dummy_data

def align_labels_with_tokens(labels, word_ids):
    new_labels = []
    current_word = None
    for word_id in word_ids:
        if word_id is None:
            new_labels.append(-100)
        elif word_id != current_word:
            new_labels.append(labels[word_id])
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
            
    logger.info("Tokenizing dataset...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    
    # Process dataset
    all_inputs = {"input_ids": [], "attention_mask": [], "labels": []}
    for item in raw_data:
        tokenized_inputs = tokenizer(item["tokens"], truncation=True, is_split_into_words=True, max_length=128)
        word_ids = tokenized_inputs.word_ids()
        
        labels = align_labels_with_tokens(item["labels"], word_ids)
        
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
