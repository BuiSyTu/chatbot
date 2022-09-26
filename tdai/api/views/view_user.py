from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import User

import json


@csrf_exempt
def users(request):
    if request.method == 'GET':
        _users = User.objects.values()

        paginator = Paginator(_users, 10)  # 10 Post trong 1 page
        page = request.GET.get('page')

        try:
            _users = paginator.page(page)
        except PageNotAnInteger:
            # trả về page đầu tiên nếu tham số page không là một số
            _users = paginator.page(1)
        except EmptyPage:
            # trả về page cuối cùng nếu page vượt ngoài số page
            _users = paginator.page(paginator.num_pages)

        return JsonResponse(list(_users), safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        User.objects.update_or_create (
            username=params.get('username'),
            password=params.get('password'),
            email=params.get('email'),
        )
        return JsonResponse({'status': 200}, safe=False)


@csrf_exempt
def user_detail(request, id):
    if request.method == 'GET':
        users = list(User.objects.filter(id=id).values())

        if not users:
            return JsonResponse(None, safe=False)

        return JsonResponse(users[0], safe=False)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        user = User.objects.get(id=id)
        user.username = params.get('username')
        user.password = params.get('password')
        user.email = params.get('email')
        user.updated_time = timezone.now()
        user.save()
        return JsonResponse({'status': 200}, safe=False)
    elif request.method == 'DELETE':
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse({'status': 200}, safe=False)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        username = params.get('username')
        password = params.get('password')

        user = User.objects.filter(username__exact=username, password__exact=password).first()

        if user is not None:
            request.session['username'] = username
            request.session['user_id'] = user.id
            return HttpResponse('Login success')
        else:
            return HttpResponse(status = 401)

        