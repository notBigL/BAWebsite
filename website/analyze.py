from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers_interpret import SequenceClassificationExplainer

model_dict = {}


# model_name = "distilbert-base-uncased-finetuned-sst-2-english"

def analyze_sentence(data, model):
    if model == 'sentiment':
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        cls_explainer = search_model(model_name)
    elif model == 'irony':
        model_name = "cardiffnlp/twitter-roberta-base-irony"
        cls_explainer = search_model(model_name)
    else:
        cls_explainer = search_model(model)

    cls_explainer(data)
    html_thingy = cls_explainer.visualize()
    print(cls_explainer.predicted_class_name, flush=True)
    print(cls_explainer.word_attributions, flush=True)
    return cls_explainer.predicted_class_name, cls_explainer.word_attributions, html_thingy


def search_model(model_name):
    if model_name in model_dict:
        return model_dict[model_name]
    else:
        print("create new model explainer")
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        cls_explainer = SequenceClassificationExplainer(model, tokenizer)

        model_dict[model_name] = cls_explainer
        return model_dict[model_name]
