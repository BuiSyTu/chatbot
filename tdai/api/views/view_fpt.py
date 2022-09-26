from tkinter import N
import requests
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def text_to_speed(request):
    if (request.method == 'POST'):
        payload = request.body
        url = 'https://api.fpt.ai/hmi/tts/v5'

        headers = {
            'api-key': 'cnnvqSxKkxOHXwJvkff681tgU7O8Gi0B',
            'speed': '',
            'voice': 'banmai'
        }

        response = requests.request('POST', url, data=payload, headers=headers)

        rs = json.loads(response.text)

        return JsonResponse(rs, safe=False)
