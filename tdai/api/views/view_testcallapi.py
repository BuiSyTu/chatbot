from tkinter import N
import requests
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def testAPI(request):
    if (request.method == 'GET'):
        url = 'https://api.fpt.ai/hmi/tts/v5'

        payload = '342424324323424'
        headers = {
            'api-key': 'cnnvqSxKkxOHXwJvkff681tgU7O8Gi0B',
            'speed': '',
            'voice': 'banmai'
        }

        response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

        rs = response.text

        return JsonResponse(rs, safe=False)
