from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    
    # контекстные переменные, передаются в шаблон
    context = {
        'title': 'MultiShop - товары на все случаи жизни',
        'content': 'Page content'
    }
    
    # функция render отрисовывает страницу
    return render(request, 'main/index.html', context)


def about(request):
    
    return HttpResponse('Информация о сайте')
