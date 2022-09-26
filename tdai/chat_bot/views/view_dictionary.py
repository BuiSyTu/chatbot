from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Dictionary


@csrf_exempt
def dictionaries(request):
    _dictionaries = Dictionary.objects.all()
    stt = 0
    for dictionary in _dictionaries:
        stt += 1
        dictionary.__setattr__('stt', stt)

    paginator = Paginator(_dictionaries, 10)  # 10 Post trong 1 page
    page = request.GET.get('page')

    try:
        _dictionaries = paginator.page(page)
    except PageNotAnInteger:
        # trả về page đầu tiên nếu tham số page không là một số
        _dictionaries = paginator.page(1)
    except EmptyPage:
        # trả về page cuối cùng nếu page vượt ngoài số page
        _dictionaries = paginator.page(paginator.num_pages)

    data = {'dictionaries': _dictionaries}
    return render(request, 'dictionaries/index.html', data)


@csrf_exempt
def add_dictionary(request):
    if request.method == 'GET':
        _dictionaries = list(Dictionary.objects.values("intent"))
        data = {
            "dictionaries": _dictionaries
        }
        return render(request, 'dictionaries/add.html', data)


@csrf_exempt
def dictionary_detail(request, id):
    if request.method == 'GET':
        dictionary = Dictionary.objects.get(id=id)
        data = {
            'dictionary': dictionary
        }
        return render(request, 'dictionaries/update.html', data)


