from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import Entity, KeyWord, Variable

def get_all(request):
    _entities = Entity.objects.all()

    # handle bot_id 
    if 'bot_id' in request.session:
        bot_id = request.session['bot_id']
        _entities = _entities.filter(bot_id__exact=bot_id)

    result = list(_entities.values())

    # hanle include
    include = request.GET.get('include', None)
    if include == 'count':
        for entity in result:
            count = len(list(KeyWord.objects.filter(entity_id=entity['id'])))
            entity['count'] = count
    return result

def create(params):
    try:
        Entity.objects.create(
            bot_id=params['bot_id'] if 'bot_id' in params else None,
            entity=params.get("entity"),
            description=params.get("description"),
            created_time=timezone.now()
        )

        Variable.objects.create(
            name=params.get("entity"),
            type="String",
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
        _entity = Entity.objects.get(id=id)
        result = model_to_dict(_entity)
        result['total_keyword'] = len(KeyWord.objects.filter(entity_id__exact=_entity.id))

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
        entity = Entity.objects.get(id=id)
        entity.entity = params.get('entity')
        entity.description = params.get('description')
        entity.updated_time = timezone.now()
        entity.save()
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
        entity = Entity.objects.get(id=id)
        entity.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }
