#!/usr/bin/env python3
"""
Scaffolding script to source a post-2025 Slovak media corpus and calibrate SlovakBERT.
Addresses the identified research gaps:
1. SlovakBERT training distribution shift (post-2025 narratives).
2. Quantifying manipulation and structural similarity across the entire media spectrum, 
   avoiding artificial dichotomies of "legitimate" vs "fake".
"""

import argparse
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_media_corpus(since_year: int = 2025) -> List[Dict]:
    """
    Scrapes narratives from various Slovak media sources to quantify similarities
    and manipulation tactics across the entire spectrum.
    """
    logger.info(f"Starting media corpus collection for narratives since {since_year}...")
    corpus = []
    
    import urllib.request
    import xml.etree.ElementTree as ET
    
    # We collect from all sources without applying arbitrary "trusted" vs "disinfo" labels
    rss_feeds = {
        "hlavnespravy.sk": "https://www.hlavnespravy.sk/feed",
        "infovojna.bz": "https://www.infovojna.bz/rss",
        "slobodnyvysielac.sk": "https://slobodnyvysielac.sk/feed/",
        "zemavek.sk": "https://zemavek.sk/feed/",
        "sme.sk": "https://primar.sme.sk/rss",
        "dennikn.sk": "https://dennikn.sk/feed/"
    }
    
    for source, url in rss_feeds.items():
        logger.info(f"Scraping {source} from {url}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                for item in root.findall('.//item'):
                    title = item.findtext('title') or ""
                    description = item.findtext('description') or ""
                    pub_date = item.findtext('pubDate') or ""
                    
                    text_content = f"{title}. {description}"
                    # No binary labels. We keep the source to later quantify similarities.
                    corpus.append({
                        "source": source,
                        "text": text_content,
                        "pub_date": pub_date
                    })
        except Exception as e:
            logger.warning(f"Failed to scrape {source}: {e}")
            
    logger.info(f"Collected {len(corpus)} total documents.")
    return corpus

def fine_tune_slovakbert(corpus: List[Dict]):
    """
    Implements unsupervised domain adaptation (Masked Language Modeling) of SlovakBERT
    on the collected corpus to resolve the distribution shift. This prepares the model
    to extract unbiased sentence embeddings (SBERT) for quantifying manipulation similarities.
    """
    if not corpus:
        logger.error("Empty corpus provided. Cannot calibrate SlovakBERT.")
        return
    
    logger.info("Initializing SlovakBERT unsupervised domain adaptation (MLM)...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForMaskedLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
        from datasets import Dataset
    except ImportError:
        logger.error("transformers or datasets library not found. Please install them.")
        return

    # Convert corpus to HuggingFace Dataset
    texts = [item.get("text", "") for item in corpus]
    hf_dataset = Dataset.from_dict({"text": texts})
    
    model_id = "gerulata/slovakbert"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], return_special_tokens_mask=True, truncation=True, max_length=128)
        
    tokenized_datasets = hf_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    
    model = AutoModelForMaskedLM.from_pretrained(model_id)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)
    
    training_args = TrainingArguments(
        output_dir="./slovakbert_adapted",
        eval_strategy="no", # We are just doing domain adaptation on the whole set
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        save_strategy="epoch"
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
        data_collator=data_collator,
    )
    
    logger.info("Starting domain adaptation (MLM)...")
    trainer.train()
    logger.info("Adaptation complete. Model saved to ./slovakbert_adapted")
    logger.info("Model is now ready for unbiased SBERT similarity clustering across all sources.")

def main():
    parser = argparse.ArgumentParser(description="Slovak Media Corpus Scraper and SlovakBERT Domain Adaptation")
    parser.add_argument("--scrape", action="store_true", help="Run the media scraper")
    parser.add_argument("--train", action="store_true", help="Run SlovakBERT domain adaptation")
    args = parser.parse_args()

    if args.scrape:
        corpus = scrape_media_corpus()
    else:
        corpus = []

    if args.train:
        fine_tune_slovakbert(corpus)

if __name__ == "__main__":
    main()
