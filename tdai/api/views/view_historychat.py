import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from chat_bot.models import Step, Intent, Scenario,HistoryChat


@csrf_exempt
def historychat(request):
    if request.method == "GET":
        _history = list(HistoryChat.objects.values())

        paginator = Paginator(_history, 10)  # 10 Post trong 1 page
        page = request.GET.get('page')

        try:
            _history = paginator.page(page)
        except PageNotAnInteger:
            # trả về page đầu tiên nếu tham số page không là một số
            _history = paginator.page(1)
        except EmptyPage:
            # trả về page cuối cùng nếu page vượt ngoài số page
            _history = paginator.page(paginator.num_pages)

        return JsonResponse(list(_history), safe=False)


@csrf_exempt
def historychat_detail(request, id):
    if request.method == 'GET':
        histories = list(HistoryChat.objects.filter(id=id).values())

        if not histories:
            return JsonResponse(None, safe=False)

        return JsonResponse(histories[0], safe=False)
    elif request.method == "PATCH":
        params = json.loads(request.body)
        history_chat = HistoryChat.objects.get(id=id)
        history_chat.value = params.get('value')
        history_chat.save()
        return JsonResponse({"status": 200}, safe=False)
    elif request.method == 'DELETE':
        history = HistoryChat.objects.get(id=id)
        history.delete()
        return JsonResponse({"status": 200}, safe=False)

