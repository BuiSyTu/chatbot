from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import KeyWord, Entity

def get_all(request):
    _keywords = KeyWord.objects.all()

    # handle bot_id
    bot_id = None
    if 'bot_id' in request.session:
        bot_id = request.session['bot_id']
        _keywords = _keywords.filter(bot_id__exact=bot_id)

    # handle entity_id
    entity_id = request.GET.get('entity_id', None)
    if entity_id is not None:
        _keywords = _keywords.filter(entity_id__exact=entity_id)

    # handle return
    data = []

    for keyword in _keywords:
        data.append({
            'id': keyword.id,
            'keyword': keyword.keyword,
            'entity_id': keyword.entity_id,
            'entity_entity': getattr(keyword.entity, 'entity', None),
            'bot_id': keyword.bot_id,
            'bot_name': getattr(keyword.bot, 'name', None)
        })
    return data

def create(params):
    try:
        KeyWord.objects.create(
            bot_id=params['bot_id'] if 'bot_id' in params else None,
            entity_id=params.get('entity_id'),
            keyword=params.get("keyword"),
            synonym=params.get("synonym"),
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
        _keyword = KeyWord.objects.get(id=id)
        result = model_to_dict(_keyword)
        result['entity_entity'] = getattr(_keyword.entity, 'entity', None)

        return {
            'status': 200,
            'message': None,
            'result': result
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e),
            'result': None
        }

def update(id, params):
    try:
        keyword = KeyWord.objects.get(id=id)
        keyword.keyword = params.get('keyword')
        keyword.synonym = params.get('synonym')
        keyword.entity_id = params.get('entity_id')
        keyword.updated_time = timezone.now()
        keyword.save()
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
        keyword = KeyWord.objects.get(id=id)
        keyword.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }
