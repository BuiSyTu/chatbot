from transformers import AutoModelForTokenClassification, pipeline
from transformers import AutoTokenizer
from underthesea import word_tokenize

# TODO: Chuyển gọi model vào phần chung
ner_model = None

try:
    model_checkpoint = "aicryptogroup/videberta-v3-base"
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = AutoModelForTokenClassification.from_pretrained("tubui7121/td-ner-bert")
    ner_model = pipeline('ner', model=model, tokenizer=tokenizer)
except Exception as e:
    print(e)

def predict_entity(sequence):
    rs = ner_model(sequence)

    res = []
    t=''
    label_set = ['O', 'ten_thu_tuc']

    for label in label_set:
        _words = ''
        score = 0
        count = 0
        obj = {}

        for item in rs:
            if item['entity'] == 'LABEL_' + str(label_set.index(label)):
                _words += item['word']
                score += item['score']
                count = count + 1

        for i in range(len(_words)):
            t = _words[0]

        _words = _words.replace(t, " ")
        _words = _words[1:]
        ls = word_tokenize(_words)
        stg = ''

        for s in ls:
            stg += "#" + s
        obj = {"keyword": stg[1:], "entity": label}

        if label != "O":
            res.append(obj)
    
    print(res)
    return res