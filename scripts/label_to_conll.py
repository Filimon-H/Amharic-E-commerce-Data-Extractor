import pandas as pd
import os

class NERLabeler:
    """
    Class for rule-based Named Entity Recognition labeling (Product, Location, Price) in Amharic.
    """

    def __init__(self):
        # Define keyword lists
    
        self.product_keywords = ["Jacket", "Sweater", "Bag", "Watch", "ጫማ", "ቁምጣ", "ሻምፒውን", "ቀሚስ", "አበሳ", "ቁርበት", "መጠጥ", "አቃጣሚ", "ቦይለር", "ጨርቅ", "ካሜራ", "መያዣ"]
        self.location_keywords = ["Addis Ababa", "AA", "Mall", "mall", "Floor", "floor", "HayaHulet", "Hayahulet", "አዲስ አበባ", "ቦሌ", "መደሐንያለም", "ህንፃ", "ፎቅ"]
        self.price_keywords = ["br", "Br", "ETB", "etb", "Price", "price", "በ", "ከ"]

    def label_text(self, text: str):
        """
        Label Amharic text tokens using keyword-based rules.

        Returns: List of "word LABEL" strings
        """
        words = text.split(' ')
        labels = []

        for index, word in enumerate(words):
            word = word.strip()

            # Price value following a price word
            if word.isnumeric():
                try:
                    if words[index - 1] in self.price_keywords:
                        labels.append("I-PRICE")
                        continue
                except IndexError:
                    pass

            # Direct keyword matches
            if word in self.price_keywords:
                if word in ["በ", "ከ"]:
                    labels.append("B-PRICE")
                else:
                    labels.append("I-PRICE")
                continue

            if word in self.location_keywords:
                labels.append("B-LOC")
                continue

            if word in self.product_keywords:
                labels.append("B-Product")
                continue

            labels.append("O")

        return list(zip(words, labels))

    def save_to_conll(self, labeled_texts, path: str):
        """
        Save list of (word, label) pairs in CoNLL format.

        Args:
            labeled_texts: List of lists of (word, label) tuples
            path: File path to save .txt
        """
        lines = []
        for sentence in labeled_texts:
            for word, label in sentence:
                lines.append(f"{word} {label}")
            lines.append("")  # blank line to separate sentences

        with open(path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))

        print(f"✅ CoNLL file saved to: {path}")

def main():
    # Load the scraped messages
    input_path = "data/telegram_data_utf8_fixed.csv"
    output_path = "data/conll_labeled2.txt"

    df = pd.read_csv(input_path, encoding="utf-8")

    # Drop empty messages and take a random sample of 40 for labeling
    df = df[['Message']].dropna().sample(30, random_state=42)

    labeler = NERLabeler()

    # Apply labeling
    df['ner_pairs'] = df['Message'].apply(labeler.label_text)

    # Save to CoNLL format
    labeler.save_to_conll(df['ner_pairs'].tolist(), output_path)

if __name__ == "__main__":
    main()
