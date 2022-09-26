from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Intent, Step
from chat_bot.utils import intent_model_helper
from tandan_nlp.classification import prediction as clf_prediction

import json


@csrf_exempt
def reply(request):
    if request.method == "POST":
        params = json.loads(request.body)
        intent_model = intent_model_helper.get_latest_model()
        text = params.get('sentence')
        reliability = clf_prediction.predict_proba_intent(text, intent_model)

        _intents = intent_model.classes_
        m = max(reliability)
        if m < 0.2:
            steps = list(Step.objects.filter(name="default answer").values())
        else:
            index = [i for i, j in enumerate(reliability) if j == m]
            intent__intent = _intents[index][0]
            intent__id = Intent.objects.get(intent=intent__intent).id
            steps = list(Step.objects.filter(intent_id=intent__id).values())
            if len(steps) == 0:
                steps = [{
                    'step_type': 0
                }]
            else:
                step_list = steps[0]['step_list']
                if step_list:
                    steps[0]['step_list'] = [int(x.strip()) for x in step_list.split(',')]
                    step_list_name = []
                    for step_id in steps[0]['step_list']:
                        temp = Step.objects.filter(id=step_id).values('name')
                        step_list_name.append(temp[0]['name'])
                    steps[0]['step_list_name'] = step_list_name
                else:
                    steps[0]['step_list'] = " "
        return JsonResponse(steps[0], safe=False)


