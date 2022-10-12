from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chat_bot.models import RequireVariables


@csrf_exempt
def requirevariables(request):
    if request.method == "GET":
        _require_variables = list(RequireVariables.objects.values())
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

