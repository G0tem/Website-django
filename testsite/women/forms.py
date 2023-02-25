from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import *

class AddPostForm(forms.ModelForm):  # класс формы. добавл статей. наслед. от базового класс Form

    def __init__(self, *args, **kwargs):  # когда форма отображается создается экземпляр формы, вызывается данный конст.
        super().__init__(*args, **kwargs)  # обяз. вызыв. конст. баз класса. чтобы выполнены автом. заполнения
        self.fields['cat'].empty_label = 'Категория не выбрана'  # для поля cat меняем свойства empty_label

    class Meta:
        model = Women  # связь формы с моделью women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']  # какие поля отобразить в форме, ('__all__'все поля кроме которых заполняют автомат)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),  # для какого поля будем определять стиль
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),  # контент предст. поле Textarea(60 колонок и 10 строчек)
        }

    def clean_title(self):  # свой валидатор начинается clean_(то поле для которого валид title)
        title = self.cleaned_data['title']  # получаем данные по заголовку, обращ к колл. cleaned_data доступна в экземпляре класса AddPostForm
        if len(title) > 200:
            raise ValidationError('Длинна превышает 200 символов')
        return title

class RegisterUserForm(UserCreationForm):  # форма рег. расширяем класс UserCreationForm
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User  # опр модель User, работает с таблицей auth_user
        fields = ('username', 'email', 'password1', 'password2')  # указ поля которые отобр в форме RegisterUserForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):  # форма предст контакты обр связь/ насл от кл формы Form общий класс для форм
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
