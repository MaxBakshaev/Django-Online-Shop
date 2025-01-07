from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q

from goods.models import Products


def q_search(query):
    """Поиск по id, словам в названии и описании"""
    
    # проверка по длине символов в поиске
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    
    # упорядочение по релевантности
    vector = SearchVector("name", "description")
    query = SearchQuery(query)
    
    return Products.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank")
    
    # # список слов в поиске для дальнейшей обработки
    # keywords = [word for word in query.split() if len(word) > 2]
    
    # q_objects = Q()
    
    # # все слова объединяются в один запрос
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)
        
    # return Products.objects.filter(q_objects)