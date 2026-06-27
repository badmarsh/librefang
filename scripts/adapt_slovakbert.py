import argparse
import logging
import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForMaskedLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

logging.basicConfig(level=logging.INFO)

class SlovakBERTAdapter:
    """
    Implements Domain-Adaptive Pretraining (DAPT) and Task-Adaptive Pretraining (TAPT)
    for SlovakBERT, based on Gururangan et al. (arXiv:2004.10964).
    """
    def __init__(self, model_name: str = "gerulata/slovakbert"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForMaskedLM.from_pretrained(model_name)
        self.is_adapted = False
        
    def _prepare_dataset(self, corpus_path: str):
        # Load line-by-line text dataset
        dataset = load_dataset("text", data_files={"train": corpus_path})
        
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"], 
                return_special_tokens_mask=True, 
                truncation=True, 
                max_length=512
            )
            
        tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["text"])
        return tokenized_datasets["train"]

    def run_dapt(self, corpus_path: str, output_dir: str = "./dapt_slovakbert") -> bool:
        """Domain-Adaptive Pretraining on large unlabeled corpus."""
        logging.info(f"Running DAPT on {corpus_path} using {self.model_name}")
        train_dataset = self._prepare_dataset(corpus_path)
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer, mlm=True, mlm_probability=0.15
        )
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=8,
            save_steps=10_000,
            save_total_limit=2,
            prediction_loss_only=True,
            fp16=torch.cuda.is_available(),
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
        )
        
        trainer.train()
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        # Update model to the DAPT one for sequential TAPT
        self.model_name = output_dir
        return True
        
    def run_tapt(self, task_dataset_path: str, output_dir: str = "./tapt_slovakbert") -> bool:
        """Task-Adaptive Pretraining on task-specific unlabeled data."""
        logging.info(f"Running TAPT on {task_dataset_path} using {self.model_name}")
        train_dataset = self._prepare_dataset(task_dataset_path)
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer, mlm=True, mlm_probability=0.15
        )
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=10, # More epochs for smaller task dataset
            per_device_train_batch_size=8,
            save_steps=5_000,
            save_total_limit=2,
            prediction_loss_only=True,
            fp16=torch.cuda.is_available(),
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
        )
        
        trainer.train()
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        self.is_adapted = True
        return True

def main():
    parser = argparse.ArgumentParser(description="Adapt SlovakBERT to post-2025 narratives")
    parser.add_argument("--dapt-corpus", type=str, help="Path to domain corpus (unlabeled text)")
    parser.add_argument("--tapt-corpus", type=str, help="Path to task corpus (unlabeled text)")
    parser.add_argument("--output-dir", type=str, default="./adapted_model", help="Where to save final model")
    args = parser.parse_args()
    
    adapter = SlovakBERTAdapter()
    if args.dapt_corpus:
        # If both are provided, DAPT output serves as input for TAPT
        dapt_out = os.path.join(args.output_dir, "dapt") if args.tapt_corpus else args.output_dir
        adapter.run_dapt(args.dapt_corpus, output_dir=dapt_out)
        
    if args.tapt_corpus:
        adapter.run_tapt(args.tapt_corpus, output_dir=args.output_dir)
        
    print(f"Adaptation complete. Model saved to {args.output_dir}")

if __name__ == "__main__":
    main()
