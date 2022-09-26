import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from chat_bot.models import Step, Card, HistoryUsedIntent

from module.module_card import check_used_intent
from module.module_variables import init_require_variables, update_variables


@csrf_exempt
def cards(request):
    if request.method == "GET":
        _cards = Card.objects.order_by('position')

        # handle step_id
        step_id = request.GET.get('step_id')
        if step_id != '0' and step_id != None:
            _cards = _cards.filter(step_id__exact=step_id)
        
        # handle card_type
        card_type = request.GET.get('card_type')
        if card_type != '0' and card_type != None:
            _cards = _cards.filter(card_type__exact=card_type)

        result = list(_cards.values())
        for card in result:
            steps = list(Step.objects.filter(id=card['step_id']).values())
            card['step'] = steps[0]

        return JsonResponse(result, safe=False)
    elif request.method == "POST":
        params = json.loads(request.body)
        status, message = check_used_intent(params)

        if not status:
            return JsonResponse({"status": 400, "message": message}, safe=False)

        if params['card_type'] =='form':
            step_id= params['step_id']
            configs = params['config']
            variables_id = []
            # Lấy variable_id cua request
            for question in configs['questions']:
                variables_id.append(question.get('variable_id'))
            bool = init_require_variables(step_id,variables_id)
            if not bool:
                return JsonResponse({"status": 400, "message": "can't find variable_id"}, safe=False)

        try:
            Card.objects.create(
                step_id=params.get('step_id'),
                name=params.get('name'),
                card_type=params.get('card_type'),
                config=json.dumps(params.get('config')),
                position=params.get('position'),
                created_time=timezone.now
            )
        except Exception as e:
            print(e)
            return JsonResponse({"status": 404, "message": "can\'t create card"}, safe=False)
        return JsonResponse({"status": 200, "message": message}, safe=False)


@csrf_exempt
def card_detail(request, id):
    if request.method == "GET":
        _cards = list(Card.objects.filter(id=id).values())

        if not _cards:
            return JsonResponse(None, safe=False)

        return JsonResponse(_cards[0], safe=False)
    elif request.method == "PUT":
        params = json.loads(request.body)

        if params.get('card_type') == 'form':
            step_id= params.get('step_id')
            configs = params.get('config')
            variables_id = []
            # Lấy variable_id cua request
            for question in configs['questions']:
                variables_id.append(question.get('variable_id'))
            bool = init_require_variables(step_id, variables_id)
            if not bool:
                return JsonResponse({"status": 400, "message": "can't find variable_id"}, safe=False)

        card = Card.objects.get(id=id)
        card.step_id = params.get('step_id')
        card.name = params.get('name')
        card.card_type = params.get('card_type')
        card.config = params.get('config')
        card.position = params.get('position')
        card.updated_time = timezone.now

        card.save()
        return JsonResponse({"status": 200}, safe=False)
    elif request.method == 'DELETE':
        card = Card.objects.get(id=id)
        card.delete()
        return JsonResponse({"status": 200}, safe=False)
    

def get_position(card):
    return card.get('position')
