from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import User


@csrf_exempt
def users(request):
    if request.method == 'GET':
        _users = User.objects.all()
        stt = 0
        for user in _users:
            stt += 1
            user.__setattr__('stt', stt)

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

        data = {'users': _users}
        return render(request, 'users/index.html', data)


@csrf_exempt
def add_user(request):
    if request.method == 'GET':
        users = list(User.objects.values('username'))
        data = {
            'users': users
        }
        return render(request, 'users/add.html', data)


@csrf_exempt
def user_detail(request, id):
    if request.method == 'GET':
        user = User.objects.get(id=id)
        data = {
            'user': user
        }
        return render(request, 'users/update.html', data)



