import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Entity, KeyWord

@csrf_exempt
def key_words(request):
    if request.method == "GET":
        _keywords = KeyWord.objects.all()

        # handle bot_id
        bot_id = None
        if 'bot_id' in request.session:
            bot_id = request.session['bot_id']
            _keywords = _keywords.filter(bot_id__exact=bot_id)

        # handle entity_id
        entity_id = request.GET.get('entity_id')
        if (entity_id is not None and entity_id != '0'):
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

        
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        # handle bot_id
        bot_id = None
        if 'bot_id' in request.session:
            bot_id = request.session['bot_id']

        params = json.loads(request.body)
        KeyWord.objects.create(
            bot_id=bot_id,
            entity_id=params.get('entity_id'),
            keyword=params.get("keyword"),
            synonym=params.get("synonym"),
            created_time=timezone.now()
        )
        return JsonResponse({"status": 200}, safe=False)


@csrf_exempt
def key_word_detail(request, id):
    if request.method == 'GET':
        keywords = list(KeyWord.objects.values())

        if not keywords:
            return JsonResponse(None, safe=False)

        keyword = keywords[0]
        entities = list(Entity.objects.filter(id=keyword['entity_id']).values())
        keyword['entity'] = entities[0]

        return JsonResponse(keyword, safe=False)
    elif request.method == "PUT":
        params = json.loads(request.body)
        keyword = KeyWord.objects.get(id=id)
        keyword.keyword = params.get('keyword')
        keyword.synonym = params.get('synonym')
        keyword.entity_id = params.get('entity_id')
        keyword.updated_time = timezone.now()
        keyword.save()
        return JsonResponse({"status": 200}, safe=False)
    elif request.method == "DELETE":
        keyword = KeyWord.objects.get(id=id)
        keyword.delete()
        return JsonResponse({"status": 200}, safe=False)
