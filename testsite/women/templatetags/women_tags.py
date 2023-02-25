from django import template
from women.models import *

register = template.Library()  # созд. экз. класса Library, через который происх. регистр. собственных шаблонных тегов

@register.simple_tag(name='getcats')  #используем декоратор класса Library, через name присваиваем имя для тега
def get_categories(filter=None):  # функция превращается в простой тег/ filter
    if not filter:
        return Category.objects.all()  # простой тег simple tags
    else:
        return Category.objects.filter(pk=filter)  # возвращаем коллекцию данных

@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):  # сортировка, какая рубрика выбрана
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, "cat_selected": cat_selected}  # включающий тег inclusion tags формирует фрагмент HTML страницы
