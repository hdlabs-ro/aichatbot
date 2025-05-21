from transformers import BertForSequenceClassification, BertTokenizerFast
import torch

class IntentClassifier:
    def __init__(self):
        self.model = BertForSequenceClassification.from_pretrained("./jupyter/my_intent_model")
        self.tokenizer = BertTokenizerFast.from_pretrained("./jupyter/my_tokenizer_model")

    def predict_intent(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        pred_label = torch.argmax(probs).item()
        labels_map = {0: "general", 1: "specific"}
        
        return labels_map[pred_label]

