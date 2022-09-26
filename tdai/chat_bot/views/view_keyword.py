from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Entity, KeyWord


@csrf_exempt
def key_words(request):
    return render(request, 'keywords/index.html')


@csrf_exempt
def add_key_words(request):
    if request.method == 'GET':
        entities = Entity.objects.all()
        keywords = list(KeyWord.objects.values("keyword"))
        data = {
            'entities': entities,
            'keywords': keywords
        }
        return render(request, 'keywords/add.html', data)


@csrf_exempt
def key_word_detail(request, id):
    if request.method == 'GET':
        keyword = KeyWord.objects.get(id=id)
        entities = Entity.objects.all()
        data = {
            'keyword': keyword,
            'entities': entities
        }
        return render(request, 'keywords/update.html', data)



