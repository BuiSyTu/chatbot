from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Entity


@csrf_exempt
def entity_types(request):
    return render(request, 'entities/index.html')


@csrf_exempt
def add_entity_types(request):
    if request.method == 'GET':
        entities = list(Entity.objects.values("entity"))
        data = {
            "entities": entities
        }
        return render(request, 'entities/add.html', data)


@csrf_exempt
def entity_type_detail(request, id):
    if request.method == 'GET':
        entity = Entity.objects.get(id=id)
        data = {
            'entity': entity
        }
        return render(request, 'entities/update.html', data)


