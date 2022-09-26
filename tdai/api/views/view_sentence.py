import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Sentence, Intent


@csrf_exempt
def sentences(request):
    if request.method == "GET":
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

        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        Sentence.objects.create(
            bot_id=request.session['bot_id'] if 'bot_id' in request.session else None,
            sentence=params.get("sentence"),
            intent_id=params.get("intent_id"),
            created_time=timezone.now()
        )
        return JsonResponse({"status": 200}, safe=False)


@csrf_exempt
def sentence_detail(request, id):
    if request.method == 'GET':
        _sentences = list(Sentence.objects.filter(id=id).values())
        if not _sentences:
            return JsonResponse(None, safe=False)
        
        sentence = _sentences[0]
        intents = list(Intent.objects.filter(id=sentence['intent_id']).values())
        sentence['intent'] = intents[0]

        return JsonResponse(sentence, safe=False)
    elif request.method == "PUT":
        params = json.loads(request.body)

        sentence = Sentence.objects.get(id=id)
        sentence.sentence = params.get('sentence')
        sentence.intent_id = params.get('intent_id')
        sentence.updated_time = timezone.now()
        sentence.save()

        return JsonResponse({"status": 200}, safe=False)
    elif request.method == "DELETE":
        sentence = Sentence.objects.get(id=id)
        sentence.delete()
        return JsonResponse({"status": 200}, safe=False)

@csrf_exempt
def sentences_excel(request):
    if request.method == 'POST':
        params = json.loads(request.body)

        data = params.get('data')
        # total = params.get('total')

        for item in data:
            Sentence.objects.create(
                bot_id=request.session['bot_id'] if 'bot_id' in request.session else None,
                sentence=item['sentence'],
                intent_id=item['intent_id'],
                created_time=timezone.now()
            )

        return JsonResponse({"status": 200}, safe=False)
