from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank, SearchVector

from goods.models import Products


def q_search(query):
    """Поиск по id, словам в названии и описании"""
    
    # проверка по длине символов в поиске
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    
    # SearchVector - запрос по нескольким полям
    vector = SearchVector("name", "description")
    # SearchQuery - поиск совпадений по всем словам
    query = SearchQuery(query)
    
    # SearchRank - упорядочение по релевантности
    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )
    
    # выделение цветом найденных слов
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )

    return result
    
    # # список слов в поиске для дальнейшей обработки
    # keywords = [word for word in query.split() if len(word) > 2]
    
    # q_objects = Q()
    
    # # все слова объединяются в один запрос
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)
        
    # return Products.objects.filter(q_objects)