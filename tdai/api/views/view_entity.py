from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Entity, KeyWord, Variable

import json


@csrf_exempt
def entity_types(request):
    if request.method == "GET":
        _entities = Entity.objects.all()

        # handle bot_id 
        if 'bot_id' in request.session:
            bot_id = request.session['bot_id']
            _entities = _entities.filter(bot_id__exact=bot_id)

        result = list(_entities.values())

        # hanle include
        include = request.GET.get('include')
        if include == 'count':
            for entity in result:
                count = len(list(KeyWord.objects.filter(entity_id=entity['id'])))
                entity['count'] = count

        return JsonResponse(result, safe=False)
    elif request.method == "POST":
        params = json.loads(request.body)
        Entity.objects.create(
            bot_id=request.session['bot_id'] if 'bot_id' in request.session else None,
            entity=params.get("entity"),
            description=params.get("description"),
            created_time=timezone.now()
        )

        Variable.objects.create(
            name=params.get("entity"),
            type="String",
            created_time=timezone.now()
        )
        return JsonResponse({"status": 200}, safe=False)


@csrf_exempt
def entity_type_detail(request, id):
    if request.method == 'GET':
        _entities = list(Entity.objects.filter(id=id).values())

        if not _entities:
            return JsonResponse(None, safe=False)

        return JsonResponse(_entities[0], safe=False)
    elif request.method == "PUT":
        params = json.loads(request.body)
        entity = Entity.objects.get(id=id)
        entity.entity = params.get('entity')
        entity.description = params.get('description')
        entity.updated_time = timezone.now()
        entity.save()
        return JsonResponse({"status": 200}, safe=False)
    elif request.method == "DELETE":
        entity = Entity.objects.get(id=id)
        entity.delete()
        return JsonResponse({"status": 200}, safe=False)

