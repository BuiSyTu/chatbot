import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from chat_bot.models import Step, Intent, Scenario,RequireVariables


@csrf_exempt
def requirevariables(request):
    if request.method == "GET":
        _require_variables = list(RequireVariables.objects.values())

        paginator = Paginator(_require_variables, 10)  # 10 Post trong 1 page
        page = request.GET.get('page')

        try:
            _require_variables = paginator.page(page)
        except PageNotAnInteger:
            # trả về page đầu tiên nếu tham số page không là một số
            _require_variables = paginator.page(1)
        except EmptyPage:
            # trả về page cuối cùng nếu page vượt ngoài số page
            _require_variables = paginator.page(paginator.num_pages)

        return JsonResponse(list(_require_variables), safe=False)


@csrf_exempt
def requirevariables_detail(request, id):
    if request.method == 'GET':
        _require_variables = list(RequireVariables.objects.filter(id=id).values())

        if not _require_variables:
            return JsonResponse(None, safe=False)

        return JsonResponse(_require_variables[0], safe=False)
    elif request.method == 'DELETE':
        require_variable = RequireVariables.objects.get(id=id)
        require_variable.delete()
        return JsonResponse({"status": 200}, safe=False)

