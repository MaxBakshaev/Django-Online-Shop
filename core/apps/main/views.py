from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    
    # контекстные переменные, передаются в шаблон
    context = {
        'title': 'Home',
        'content': 'Page content'
    }
    
    # функция render отрисовывает страницу
    return render(request, 'main/index.html', context)


def about(request):
    
    return HttpResponse('Информация о сайте')
