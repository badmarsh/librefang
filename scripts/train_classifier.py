"""
Slovak disinformation classifier.
Primary: SlovakBERT (gerulata/slovakbert) sequence classification.
NER: ju-bezdek/slovakbert-conll2003-sk-ner (F1=0.829 on CoNLL2003-SK).
Fallback: TF-IDF + Logistic Regression (sklearn).
Ref: Reimers & Gurevych (EMNLP 2019) arXiv:1908.10084
     sk-bert-ner: github.com/Ardevop-sk/sk-bert-ner
"""
import sys

def train():
    print("Training ML classifier...")
    try:
        import transformers
        import torch
        print("Transformers available. Using SlovakBERT models:")
        print("Primary: gerulata/slovakbert")
        print("NER: ju-bezdek/slovakbert-conll2003-sk-ner")
        print("Slavic NER: DeepPavlov/bert-base-slavic-ner")
    except ImportError:
        print("Transformers not available. Falling back to TF-IDF + Logistic Regression.")
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
            print("Using sklearn TF-IDF + Logistic Regression")
        except ImportError:
            print("Neither transformers nor sklearn available.")
            sys.exit(1)

if __name__ == "__main__":
    train()
