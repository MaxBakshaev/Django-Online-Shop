from django.db.models import Q

from goods.models import Products


def q_search(query):
    
    # проверка по длине символов в поиске
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    
    # список слов в поиске для дальнейшей обработки
    keywords = [word for word in query.split() if len(word) > 2]
    
    q_objects = Q()
    
    # все слова объединяются в один запрос
    for token in keywords:
        q_objects |= Q(description__icontains=token)
        q_objects |= Q(name__icontains=token)
        
    return Products.objects.filter(q_objects)