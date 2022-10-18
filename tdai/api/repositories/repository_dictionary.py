from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import Dictionary

def get_all(request):
    _dictionaries = Dictionary.objects.all()

    # hanle bot_id
    if 'bot_id' in request.session:
        bot_id = request.session.get('bot_id')
        _dictionaries = _dictionaries.filter(bot_id__exact=bot_id)

    return list(_dictionaries.values())

def create(params):
    try:
        Dictionary.objects.create(
            word=params.get('word'),
            synonym=params.get('synonym'),
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
        dictionary = Dictionary.objects.get(id=id)
        result = model_to_dict(dictionary)

        return {
            "status": 200,
            "result": result,
            "message": None
        }
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "result": None
        }

def update(id, params):
    try:
        dictionary = Dictionary.objects.get(id=id)
        dictionary.word = params.get('word')
        dictionary.synonym = params.get('synonym')
        dictionary.updated_time = timezone.now()
        dictionary.save()
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
        dictionary = Dictionary.objects.get(id=id)
        dictionary.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }
