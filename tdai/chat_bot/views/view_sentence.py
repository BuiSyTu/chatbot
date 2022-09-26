from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Sentence, Intent


@csrf_exempt
def sentences(request):
    if request.method == "GET":
        return render(request, 'sentences/index.html')


@csrf_exempt
def add_sentences(request):
    if request.method == 'GET':
        _intents = list(Intent.objects.values())
        _sentences = list(Sentence.objects.values("sentence"))

        data = {
            'intents': _intents,
            'sentences': _sentences
        }
        return render(request, 'sentences/add.html', data)


@csrf_exempt
def sentence_detail(request, id):
    if request.method == 'GET':
        sentence = Sentence.objects.get(id=id)
        _intents = Intent.objects.all()
        data = {
            'sentence': sentence,
            'intents': _intents
        }
        return render(request, 'sentences/update.html', data)
