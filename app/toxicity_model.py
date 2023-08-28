from typing import Tuple

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline


class ToxicityDetector:
    def __init__(self):
        self.model_path = "martin-ha/toxic-comment-model"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        self.pipeline = TextClassificationPipeline(model=self.model, tokenizer=self.tokenizer)

    def predict(self, text: str) -> Tuple[bool, float]:
        is_toxic, toxicity_score = self.pipeline(text)[0]['label'], self.pipeline(text)[0]['score']
        is_toxic = True if is_toxic == 'toxic' else False
        return is_toxic, toxicity_score
