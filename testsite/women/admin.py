from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')  # спис. тех полей, которые хотим в админ панели
    list_display_links = ('id', 'title')  # те поля на которые можно кликнуть для редакт
    search_fields = ('title', 'content')  # по каким полям можно производить поиск информ.
    list_editable = ("is_published",)  # список полей которые редактируемы
    list_filter = ('is_published', 'time_create')  # те поля по которым сможем фильтровать список статей
    prepopulated_fields = {'slug': ('title',)}  # атрибут заполнять автом. слаг на основе title
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'is_published', 'get_html_photo', 'time_create', 'time_update')  # все редактируемые поля
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # не редактируемые поля
    save_on_top = True  # сохр в верхней части

    def get_html_photo(self, object):  # форм html код, object ссылается на текущ запись
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")  # mark_safe не экранировать код/ width=50 размер

    get_html_photo.short_description = 'Миниатюра'  # имя колонки в админ панели с картинками

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # спис. тех полей, которые хотим в админ панели
    list_display_links = ('id', 'name')  # те поля на которые можно кликнуть для редакт
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # атрибут заполнять автом. слаг на основе name


admin.site.register(Women, WomenAdmin)  # использ пакет admin, обращаемся к ветке сайт, вызываем функц. регистер (указываем ту модель которую хотем рег в админ панели)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'  # переопр названия в админ панели
admin.site.site_header = 'Админ-панель сайта о женщинах1'