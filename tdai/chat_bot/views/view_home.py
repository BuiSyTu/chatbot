from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    if request.method == "GET":
        return redirect("/sentences/")

@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'login/index.html')