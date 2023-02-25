from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView  # импорт класса ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'  # путь к шаблону
    context_object_name = 'posts'  # имя для обращения в шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # обращ к базовому кл.ListView и взять у него сущест контекст
        c_def = self.get_user_context(title='Главная страница')  # на основе DataMixin
        return dict(list(context.items()) + list(c_def.items()))  # формируем общ контекст на основе 2 словарей

    def get_queryset(self):  # что именно выбирать из модели Women
        return Women.objects.filter(is_published=True).select_related('cat')  # чит те запис для кот is_published=True / добавл .select_related('cat') для жадной загрузки чтобы убрать дубли SQL запр


def about(request):
    contact_list = Women.objects.all()  # пример пагинации через функц представ// читаем спис всех женщ
    paginator = Paginator(contact_list, 3)  # Самостоят созд экз класса пагинатор

    page_number = request.GET.get('page')  # получ № стр из гет запроса
    page_obj = paginator.get_page(page_number)  # форм спис элем текущ стр. ниже перед список нашему шабл
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm  # указ класс формы который будет связан с классом представления AddPage
    template_name = 'women/addpage.html'
    seccess_url = reverse_lazy('home')  # если в модели не пропис метод get_absolute_url, указ адрес маршрута на который должны перенапр когда добавляем статью, reverse_lazy выполняет построения маршрута когда он понадобится
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')  # на основе DataMixin
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):  # насл. от датамиксин и FormView станд класс для форм которые не превязаны к модели
    form_class = ContactForm  # ссылка на класс
    template_name = 'women/contact.html'  # шаблон
    success_url = reverse_lazy('home')  # если форм успешно заполненна перенапр на гл стр

    def get_context_data(self, *, object_list=None, **kwargs):  # форм контекст для шаблона
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # вызывается в том случае если верно заполнили все поля форм
        print(form.cleaned_data)
        return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # прописывается перем для слага для использ
    context_object_name = 'post'  # в какую перем, будут помещатся данные из модели women для использ в шаблонах

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # будет появляться 404 если страница не найдена

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')  # выбрать из табл women записи для которых слаг совподает со слагом категории связонной с это запись и статья опублик

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)

        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):  # так как раб с форм. насл от CreateView и нашего миксина
    form_class = RegisterUserForm  # ссылается на свою форму
    template_name = 'women/register.html'  # ссылка на шаблон
    success_url = reverse_lazy('login')  # перенаправлени на юрл адрес при успешной регистрации

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # вызывается при успешной проверке формы регистрации
        user = form.save()  # сохр форму в БД
        login(self.request, user)  # вызов спец функ котор авториз пользов (обьект request, данные рег польз)
        return redirect('home')

class LoginUser(DataMixin, LoginView):  # насл LoginView встроенный клас со всей логикой авториз
    form_class = LoginUserForm  # ссылается на свою форму
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):  # метод будет вызываться если верно ввели лог и пароль
        return reverse_lazy('home')  # перенаправление на

def logout_user(request):  # выход из аккаунта
    logout(request)  # вызов станд. джанговск функ чтобы пользов мог выйти
    return redirect('login')
