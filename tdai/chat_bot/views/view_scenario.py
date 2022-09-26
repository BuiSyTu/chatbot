from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import  render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Scenario
from chat_bot.utils import intent_model_helper, entity_model_helper
from tandan_nlp.classification import prediction as clf_prediction
from tandan_nlp.ner import prediction as ner_prediction


@csrf_exempt
def scenarios(request):
    if request.method == 'GET':
        return render(request, 'scenarios/index.html')


@csrf_exempt
def add_scenario(request):
    if request.method == 'GET':
        return render(request, 'scenarios/add.html')


@csrf_exempt
def scenario_detail(request, id):
    if request.method == 'GET':
        scenario = Scenario.objects.get(id=id)

        data = {
            'scenario': scenario,
        }

        return render(request, 'scenarios/update.html', data)

