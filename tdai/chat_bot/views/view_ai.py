import pickle

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LogisticRegression

from chat_bot.models import Sentence, Intent, Entity, KeyWord, IntentModel, EntityModel
from chat_bot.utils import intent_model_helper, entity_model_helper
from tandan_nlp.classification import trainer as clf_trainer, prediction as clf_prediction
from tandan_nlp.ner import reader, trainer as ner_trainer, prediction_bert as ner_prediction
from tandan_nlp.util.check_date import check_date

from pyvi.ViTokenizer import ViTokenizer


@csrf_exempt
def training(request):
    if request.method == "GET":
        # training intent
        sentences = Sentence.objects.all()
        sentences__sentence = []
        _intents = []
        for sentence in sentences:
            intent_id = sentence.intent_id
            intent = Intent.objects.get(id=intent_id)
            _intents.append(intent.intent)
            sentences__sentence.append(sentence.sentence)
        x_train, y_train = clf_trainer.get_train_data(sentences__sentence, _intents)
        intent_model = clf_trainer.training(clf_trainer.get_model(classifier=LogisticRegression()), x_train, y_train)
        intent_model_dump = pickle.dumps(intent_model)
        IntentModel.objects.create(
            bot_id=3,
            data=intent_model_dump,
            created_time=timezone.now()
        )

        # training entity
        # words = []
        # entities = []
        # keywords = KeyWord.objects.all()
        # for keyword in keywords:
        #     entity = Entity.objects.get(id=keyword.entity_id)
        #     words.append(keyword.keyword)
        #     entities.append(entity.entity)
        # features = []
        # for sentence in sentences:
        #     feature = []
        #     word_features, pos_features, entity_features = reader.read_entities(sentence.sentence, words, entities)
        #     [feature.append((word_features[i], pos_features[i], entity_features[i])) for i in range(len(word_features))]
        #     features.append(feature)
        # x_train, y_train = ner_trainer.get_train_data(features)
        # entity_model = ner_trainer.training(x_train, y_train)
        # print(entity_model)
        # entity_model_dump = pickle.dumps(entity_model)
        # EntityModel.objects.create(
        #     bot_id=3,
        #     data=entity_model_dump,
        #     created_time=timezone.now()
        # )
        return JsonResponse({"type": "POST"}, safe=False)


@csrf_exempt
def test_nlp(request):
    if request.method == 'GET':
        return render(request, 'test_nlp/index.html')
    if request.method == 'POST':
        sentence = request.POST.get('sentence')
        text = sentence.strip()
        # predict intent
        intent_model = intent_model_helper.get_latest_model()
        reliability = clf_prediction.predict_proba_intent(text, intent_model)
        _intents = intent_model.classes_
        rs_intent = []
        for i, intent in enumerate(_intents):
            rs_intent.append({
                'intent': intent,
                'reliability': round(reliability[i] * 100, 2)
            })
        rs_intent = sorted(rs_intent, key=lambda x: x.get('reliability'), reverse=True)
        if len(rs_intent) > 4:
            rs_intent = rs_intent[:4]

        # predict entity
        # entity_model = entity_model_helper.get_latest_model()
        # entities = ner_prediction.predict_entity(text, entity_model)
        # rs_entity = []
        # for entity in entities:
        #     rs_entity.append({
        #         'keyword': entity[0],
        #         'entity': entity[2]
        #     })

        # tokenize_text = ViTokenizer.tokenize(text)
        # dates = check_date(tokenize_text)
        # for date in dates:
        #     rs_entity.append({
        #         'keyword': date,
        #         'entity': 'thoi_gian'
        #     })
        rs_entity = ner_prediction.predict_entity(text)

        data = {
            'status': 200,
            'sentence': text,
            'intents': rs_intent,
            'entities': rs_entity
        }
        return render(request, 'test_nlp/index.html', data)


@csrf_exempt
def speech_to_text(request):
    return render(request, 'speech_to_text.html')
