# Amharic-E-commerce-Data-Extractor
Transform messy Telegram posts into a smart FinTech engine that reveals which vendors are the best candidates for a loan.
# 📦 EthioMart: Amharic E-commerce Data Extractor (Tasks 1 & 2)

> **Project Dates:** 18–24 June 2025  
> **Goal:** Transform messy Telegram messages into structured product, price, and location data using fine-tuned NER models on Amharic text.

---

## 🚀 Overview

EthioMart aims to centralize Ethiopia’s fragmented Telegram-based e-commerce market by extracting structured insights (products, prices, locations) from unstructured Amharic posts. These insights will feed into a smart FinTech engine that supports vendor evaluation, product tracking, and credit risk scoring.

This repo covers:

- ✅ **Task 1:** Amharic Telegram message ingestion + preprocessing  
- ✅ **Task 2:** Manual labeling of 30–50 messages using the CoNLL format for NER model fine-tuning

---

## 🛠️ Task 1 – Data Ingestion & Preprocessing

### ✅ Steps Completed

1. **Selected Channels:** Scraped 5+ e-commerce Telegram channels (e.g., `@Shageronlinestore`, `@EthioStyle`, etc.).
2. **Telegram Scraper:** Used Python-based Telethon script for message collection.
3. **Preprocessing Pipeline:** 
   - Removed emojis, links, metadata
   - Tokenized Amharic text using `spacy` and `transformers`
   - Normalized unicode + custom handling for mixed-script messages
4. **Storage:** Cleaned data stored as structured `.json` and `.csv` for annotation and model training.

---

## 🏷️ Task 2 – Manual NER Labeling (CoNLL Format)

### ✅ Entity Tags Used

| Tag         | Description                                |
|-------------|--------------------------------------------|
| `B-Product` | Start of a product name                    |
| `I-Product` | Inside a product name                      |
| `B-PRICE`   | Start of a price (e.g., "100 ብር")          |
| `I-PRICE`   | Inside a price entity                     |
| `B-LOC`     | Start of a location (e.g., "Addis Abeba") |
| `I-LOC`     | Inside a location name                    |
| `O`         | Outside any entity                         |

### ✅ Annotation Format

- Used CoNLL standard: one token per line with entity tag  
- Blank line separates sentences  
- Saved 30+ fully labeled Amharic messages as `amharic_ner_conll.txt`

---

## ⚙️ Tools & Environment

- **Colab:** Used for model training and fast experimentation
- **Hugging Face Transformers**
- **Telethon / BeautifulSoup**
- **Python 3.11**, `pandas`, `spacy`, `re`

---

## 🧠 Challenges & Solutions

| Challenge                        | Solution                                             |
|----------------------------------|------------------------------------------------------|
| Amharic tokenization issues      | Used multilingual tokenizer (`xlm-roberta-base`)    |
| Telegram rate limits             | Added timeouts + retries in scraper                 |
| Labeling ambiguity in pricing    | Built context-based labeling guidelines             |

---

## 🔭 Next Steps

🔜 **Task 3:** Fine-tune `xlm-roberta-base` on our labeled dataset  
🔜 **Task 4:** Evaluate, compare with `bert-tiny-amharic` and `afroxlmr-large`  
🔜 **Task 5:** Visualize predictions, interpret with SHAP/LIME, recommend best model

---


**Prepared by:** Filimon Haylemriyam

📅 Final Submission: June 2025
