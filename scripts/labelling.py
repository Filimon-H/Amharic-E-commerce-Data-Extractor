import pandas as pd
import re

class NERLabeler:
    """
    Rule-based Named Entity Recognition labeler for Amharic e-commerce data.
    Supports multi-word entities and correct B-/I- tagging.
    """

    def __init__(self):
        self.product_keywords = ["Baby bottle", "Jacket", "Sweater", "Bag", "Watch", "ጫማ", "ቁምጣ", "ሻምፒውን", "ቀሚስ", "አበሳ", "ቁርበት", "መጠጥ", "አቃጣሚ", "ቦይለር", "ጨርቅ", "ካሜራ", "መያዣ"]
        self.location_keywords = ["Addis Ababa", "AA", "Mall", "mall", "Floor", "floor", "HayaHulet", "Hayahulet", "አዲስ አበባ", "ቦሌ", "መደሐንያለም", "ህንፃ", "ፎቅ"]
        self.price_keywords = ["ዋጋ", "price", "Price", "በ", "ከ", "ETB", "etb", "Br", "br", "ብር"]

    def clean_text(self, text):
        # Remove emojis, punctuation (except ብር, በ), and extra spaces
        text = re.sub(r'[^\w\sብርበከ]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def label_text(self, text: str):
        text = self.clean_text(text)
        words = text.split()
        labels = ["O"] * len(words)

        def apply_entity(entity_list, b_label, i_label):
            for entity in entity_list:
                entity_words = entity.split()
                for i in range(len(words) - len(entity_words) + 1):
                    if words[i:i+len(entity_words)] == entity_words:
                        labels[i] = b_label
                        for j in range(1, len(entity_words)):
                            labels[i + j] = i_label

        # Apply labeling rules
        apply_entity(self.location_keywords, "B-LOC", "I-LOC")
        apply_entity(self.product_keywords, "B-Product", "I-Product")

        # Price entities: B-PRICE then I-PRICE for number and ብር
        for i in range(len(words)):
            if words[i] in self.price_keywords:
                labels[i] = "B-PRICE"
                if i + 1 < len(words) and words[i + 1].isnumeric():
                    labels[i + 1] = "I-PRICE"
                if i + 2 < len(words) and words[i + 2] in ["ብር", "ETB", "Br"]:
                    labels[i + 2] = "I-PRICE"

        return list(zip(words, labels))

    def save_to_conll(self, labeled_texts, path: str):
        lines = []
        for sentence in labeled_texts:
            for word, label in sentence:
                lines.append(f"{word} {label}")
            lines.append("")  # Sentence separator

        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"✅ CoNLL file saved to: {path}")




def main():
    input_path = "data/telegram_data_utf8_fixed.csv"
    output_path = "data/conll_labeled.txt"

    df = pd.read_csv(input_path, encoding="utf-8")
    df = df[['Message']].dropna().sample(30, random_state=42)

    labeler = NERLabeler()
    df['ner_pairs'] = df['Message'].apply(labeler.label_text)
    labeler.save_to_conll(df['ner_pairs'].tolist(), output_path)

if __name__ == "__main__":
    main()



