# from favorites.models import Favorite


# def get_user_favorites(request):
#     if request.user.is_authenticated:
#         return Favorite.objects.filter(user=request.user).select_related('product')

#     # если пользователь не авторизован, то создается сессионный ключ
#     if not request.session.session_key:
#         request.session.create()
#     return Favorite.objects.filter(session_key=request.session.session_key).select_related('product')
