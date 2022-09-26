from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import  render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Step, Intent, Scenario
from chat_bot.utils import intent_model_helper, entity_model_helper
from tandan_nlp.classification import prediction as clf_prediction
from tandan_nlp.ner import prediction_bert as ner_prediction


@csrf_exempt
def steps(request):
    if request.method == "GET":
        return render(request, 'steps/index.html')


@csrf_exempt
def add_steps(request):
    if request.method == 'GET':
        scenarios = Scenario.objects.all()

        data = {
            'scenarios': scenarios
        }

        return render(request, 'steps/add.html', data)


@csrf_exempt
def step_detail(request, id):
    if request.method == 'GET':
        _steps = Step.objects.all()
        step = Step.objects.get(id=id)
        scenarios = Scenario.objects.all()

        data = {
            'step': step,
            'scenarios': scenarios,
        }
        return render(request, 'steps/update.html', data)


@csrf_exempt
def reply_step(request):
    if request.method == 'GET':
        return render(request, 'step/message.html')
    if request.method == "POST":
        sentence = request.POST.get('sentence')
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

        # predict entity
        # entity_model = entity_model_helper.get_latest_model()
        # entities = ner_prediction.predict_entity(sentence, entity_model)
        entities = ner_prediction.predict_entity(sentence)
        rs_entity = []
        for entity in entities:
            rs_entity.append({
                'keyword': entity[0],
                'entity': entity[2]
            })
        data = {
            'status': 200,
            'sentence': sentence,
            'intents': rs_intent,
            'entities': rs_entity
        }

    return render(request, 'step/message.html', data)
