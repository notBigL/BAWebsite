from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers_interpret import SequenceClassificationExplainer


def analyze_sentiment(data):
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    cls_explainer = SequenceClassificationExplainer(model, tokenizer)
    cls_explainer(data)

    print(cls_explainer.predicted_class_name, flush=True)
    print(cls_explainer.word_attributions, flush=True)
    return cls_explainer.predicted_class_name


def analyze_irony(data):
    model_name = "cardiffnlp/twitter-roberta-base-irony"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    cls_explainer = SequenceClassificationExplainer(model, tokenizer)
    cls_explainer(data)

    print(cls_explainer.predicted_class_name, flush=True)
    print(cls_explainer.word_attributions, flush=True)
