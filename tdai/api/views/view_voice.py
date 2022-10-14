from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.services import service_voice

@csrf_exempt
def text_to_speed(request):
    if (request.method == 'POST'):
        payload = request.body
        rs = service_voice.get_voice(text=payload)
        return JsonResponse(rs, safe=False)
