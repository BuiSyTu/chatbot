import json
import pickle

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from pyvi.ViTokenizer import ViTokenizer
from sklearn.linear_model import LogisticRegression

from chat_bot.models import Sentence, Intent, Entity, KeyWord, IntentModel, EntityModel
from chat_bot.utils import intent_model_helper, entity_model_helper
from tandan_nlp.classification import trainer as clf_trainer, prediction as clf_prediction
from tandan_nlp.ner import reader, trainer as ner_trainer, prediction_bert as ner_prediction
from tandan_nlp.util.check_date import check_date


@csrf_exempt
def training(request):
    if request.method == "GET":
        bot_id = request.GET.get('bot_id')

        sentences = Sentence.objects.filter(bot_id=bot_id)
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
            bot_id=bot_id,
            data=intent_model_dump,
            created_time=timezone.now()
        )
        return JsonResponse({"status": "200"}, safe=False)


@csrf_exempt
def test_nlp(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        sentence = params.get('sentence')
        # predict intent
        intent_model = intent_model_helper.get_latest_model()
        reliability = clf_prediction.predict_proba_intent(sentence, intent_model)
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

        rs_entity = ner_prediction.predict_entity(sentence)

        data = {
            'intents': rs_intent,
            'entities': rs_entity
        }
        return JsonResponse(data, safe=False)

