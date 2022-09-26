from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

#from chat_bot.models import User

@csrf_exempt
def test(request):
    if request.method == 'GET':
        return render(request, 'components/card/clear_memory.html')