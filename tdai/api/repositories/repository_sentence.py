from django.utils import timezone

from chat_bot.models import Intent, Sentence

def get_all(request):
    _sentences = Sentence.objects.all()

    # handle bot_id
    if 'bot_id' in request.session:
        bot_id = request.session['bot_id']
        _sentences = _sentences.filter(bot_id__exact=bot_id)

    # handle intent_id
    intent_id = request.GET.get('intent_id')
    if intent_id != None and intent_id != '0':
        _sentences = _sentences.filter(intent_id__exact=intent_id)

    result = list(_sentences.values())
    for sen in result:
        intents = list(Intent.objects.filter(id=sen['intent_id']).values())
        if (len(intents) > 0):
            sen['intent'] = intents[0]
    return result

def create(params):
    try:
        Sentence.objects.create(
            bot_id=params['bot_id'] if 'bot_id' in params else None,
            sentence=params.get("sentence"),
            intent_id=params.get("intent_id"),
            created_time=timezone.now()
        )
        return {
            'status': 201,
            'message': 'Thêm thành công'
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }

def get_by_id(id):
    try:
        _sentence = Sentence.objects.get(id=id)
    except Exception as e:
        return {
            'status': 500,
            'message': str(e),
            'result': None
        }

    result = {
        'id': _sentence.id,
        'sentence': _sentence.sentence,
        'intent_id': _sentence.intent_id,
        'intent_intent': getattr(_sentence.intent, 'intent', None),
        'bot_id': _sentence.bot_id,
        'bot_name': getattr(_sentence.bot, 'name', None)
    }

    return {
        'status': 200,
        'message': None,
        'result': result
    }

def update(id, params):
    try:
        sentence = Sentence.objects.get(id=id)
        sentence.sentence = params.get('sentence')
        sentence.intent_id = params.get('intent_id')
        sentence.updated_time = timezone.now()
        sentence.save()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }

def delete(id):
    try:
        sentence = Sentence.objects.get(id=id)
        sentence.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }
