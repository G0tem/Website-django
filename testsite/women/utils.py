from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]

class DataMixin:
        paginate_by = 3  # кол. элем на одной стр
        def get_user_context(self, **kwargs):
                context = kwargs

                cats = cache.get('cats')  # кеш
                if not cats:
                    cats = Category.objects.annotate(Count('women'))  # чтобы выводить в шаблоне только те рубр у которых есть посты
                    cache.set('cats', cats, 60)  # кеш

                user_menu = menu.copy()
                if not self.request.user.is_authenticated:  # у кл. DataMixin есть обьект request у него есть обьект user а у него is_authenticated если true авториз
                        user_menu.pop(1)  # если польз не авториз. удаляем с сайта пункт доб.статьи

                context['menu'] = user_menu

                context['cats'] = cats
                if 'cat_selected' not in context:
                        context['cat_selected'] = 0
                return context