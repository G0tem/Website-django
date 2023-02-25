from django.db import models
from django.urls import reverse

class Women(models.Model):  #Model базовый класс / verbose_name='' как отображаются в админ панели и на сайте
    title = models.CharField(max_length=255, verbose_name='Заголовок')  # класс CharField определяет текстовое поле n-длинны
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')  # в джанго спец класс SlagField/макс длинна, уникальное=True,индексируемое
    content = models.TextField(blank=True, verbose_name='Текст статьи')  # (большое текстовое поле blank=True может быть пустым
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')  # в какой каталог будем загружать фото(опр в виде шаблона, подкаталог фото/год/мес./день
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')  # время создания статьи, auto_now_add = берет авт. время. когда создали и не меняется
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')  # время редактирования статьи auto_now= авт. меняет время когда изменили
    is_published = models.BooleanField(default=True, verbose_name='Публикация')  # булево поле, автоматически принимает труе когда добавили запись
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')  #добавим внешний ключ cat'_id' добавит автоматом. используем класс ForeignKey(указ первичную категорию как строку название класса, models.PROTECT) , related_name='get_posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:  # Вложенный класс для настройки отображения в админ панели и на сайте
        verbose_name = 'Известные женщины'  # имя статей
        verbose_name_plural = 'Известные женщины'  # имя множ.число
        ordering = ['-time_create', 'title']  # Порядок сортировки статей в админ панели и НА САЙТЕ

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id'] 
