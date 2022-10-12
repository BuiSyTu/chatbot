import json

from django.utils import timezone

from chat_bot.models import Card, Step, HistoryUsedIntent
from api.repositories import repository_variable

def get_all(request):
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

    return result

def create(params):
    status = check_used_intent(params)

    if not status:
        return {
            'status': 400,
            'message': 'intent was used'
        }

    if params['card_type'] =='form':
        step_id= params['step_id']
        configs = params['config']
        variables_id = []
        # Lấy variable_id cua request
        for question in configs['questions']:
            variables_id.append(question.get('variable_id'))

        repository_variable.init_require_variables(step_id, variables_id)

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
        return {
            'status': 500,
            'message': str(e)
        }

    return {
        'status': 200,
        'message': 'Thêm thành công'
    }

# TODO: check lại luồng xử lý hàm này
def check_used_intent(request):
    config = request.get('config')

    if request.get('card_type') != 'intent':
        return True

    try:
        intent_id = int(config.get('intent_id'))
        history = list(HistoryUsedIntent.objects.filter(intent_id=intent_id).values())

        if len(history) > 0:
            return False
        else:
            HistoryUsedIntent.objects.create(
                step_id=request['step_id'],
                intent_id=intent_id
            )
            return True
    except Exception as e:
        print(e)
        return True

def get_by_id(id):
    try:
        card = Card.objects.get(id=id)
    except Exception as e:
        return {
            "status": 400,
            "message": str(e),
            "result": None
        }

    result = {
        'id': card.id,
        'step_id': card.step_id,
        'card_type': card.card_type,
        'name': card.name,
        'config': json.loads(card.config),
        'position': card.position,
        'created_time': card.created_time,
        'updated_time': card.updated_time
    }

    return {
        "status": 200,
        "result": result,
        "message": None
    }

def update(id, params):
    try:
        card = Card.objects.get(id=id)
        config = params.get('config')

        card.step_id = params.get('step_id')
        card.name = params.get('name')
        card.card_type = params.get('card_type')
        card.config = json.dumps(config)
        card.position = params.get('position')
        card.updated_time = timezone.now

        card.save()
        return {
            "status": 204,
            "message": "Thành công"
        }
    except Exception as e:
        return {
            "status": 500,
            "message": str(e)
        }

def delete(id):
    try:
        card = Card.objects.get(id=id)
        card.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }

def get_by_step_id(step_id):
    cards = list(Card.objects.filter(step_id=step_id).values())
    try:
        cards = sorted(cards, key=lambda k: k.get('position', 1000), reverse=False)
        return cards
    except Exception as e:
        print(e)
        return []