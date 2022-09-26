from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Variable


@csrf_exempt
def variables(request):
    if request.method == 'GET':
        _variables = Variable.objects.all()
        stt = 0
        for variable in _variables:
            stt += 1
            variable.__setattr__('stt', stt)

        paginator = Paginator(_variables, 10)  # 10 Post trong 1 page
        page = request.GET.get('page')

        try:
            _variables = paginator.page(page)
        except PageNotAnInteger:
            # trả về page đầu tiên nếu tham số page không là một số
            _variables = paginator.page(1)
        except EmptyPage:
            # trả về page cuối cùng nếu page vượt ngoài số page
            _variables = paginator.page(paginator.num_pages)

        data = {'variables': _variables}
        return render(request, 'variables/index.html', data)


@csrf_exempt
def add_variable(request):
    if request.method == 'GET':
        variables = list(Variable.objects.values())
        data = {
            'variables': variables
        }

        return render(request, 'variables/add.html', data)


@csrf_exempt
def variable_detail(request, id):
    if request.method == 'GET':
        return render(request, 'variables/update.html')



