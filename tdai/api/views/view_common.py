import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.services import service_common


@csrf_exempt
def get_current_date(request):
    if request.method == 'GET':
        answers = [{
            'card_type': 'text',
            'buttons': [],
            'text': service_common.get_current_date()
        }]
        return JsonResponse(answers, safe=False)