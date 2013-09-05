from django.http import HttpResponse


def errorView404(request):
    return HttpResponse("PAGE NOT FOUND! 404 ERROR")


def errorView500(request):
    return HttpResponse("500 INTERNAL SERVER ERROR")
