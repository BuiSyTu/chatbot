import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chat_bot.models import HistoryChat


@csrf_exempt
def historychat(request):
    if request.method == "GET":
        _history = list(HistoryChat.objects.values())
        return JsonResponse(list(_history), safe=False)


@csrf_exempt
def historychat_detail(request, id):
    if request.method == 'GET':
        histories = list(HistoryChat.objects.filter(id=id).values())

        if not histories:
            return JsonResponse(None, safe=False)

        return JsonResponse(histories[0], safe=False)
    elif request.method == "PUT":
        params = json.loads(request.body)
        history_chat = HistoryChat.objects.get(id=id)
        history_chat.value = params.get('value')
        history_chat.save()
        return JsonResponse({"status": 200}, safe=False)
    elif request.method == 'DELETE':
        history = HistoryChat.objects.get(id=id)
        history.delete()
        return JsonResponse({"status": 200}, safe=False)

