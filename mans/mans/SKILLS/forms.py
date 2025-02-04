from django import forms
from django.core.exceptions import ValidationError
from .models import User, Comment
from django.contrib.auth import get_user_model


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}), label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}), label="Подтверждение пароля")

    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес электронной почты'})
        }
        labels = {
            'username': 'Имя',
            'phone': 'Номер',
            'email': 'Почта'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Проверка паролей на совпадение
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")

        # Проверка уникальности поля email
        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким адресом электронной почты уже существует.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Хранить пароль в зашифрованном виде
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Имя пользователя или почта", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваши данные'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}), label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username_or_email or not password:
            raise forms.ValidationError("Имя пользователя и пароль обязательны для ввода.")

        # Поиск пользователя по username или email
        User = get_user_model()
        user = None
        if "@" in username_or_email:
            user = User.objects.filter(email=username_or_email).first()  # Используем email
        else:
            user = User.objects.filter(username=username_or_email).first()

        if user is None:
            raise forms.ValidationError("Пользователь с таким именем или электронной почтой не найден.")

        # Проверка пароля
        if not user.check_password(password):
            raise forms.ValidationError("Неверный пароль.")

        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'profile_image']
        widgets = {
            'email': forms.TextInput(attrs={
                'style': 'resize: none; width: 200px; height: 30px; border: 1px solid black; border-radius: 5px; padding: 10px;'
            }),
            'phone': forms.NumberInput(attrs={
                'style': 'resize: none; width: 200px; height: 30px; border: 1px solid black; border-radius: 5px; padding: 10px;'
            }),
            'last_name': forms.TextInput(attrs={
                'style': 'resize: none; width: 200px; height: 30px; border: 1px solid black; border-radius: 5px; padding: 10px;'
            }),
            'first_name': forms.TextInput(attrs={
                'style': 'resize: none; width: 200px; height: 30px; border: 1px solid black; border-radius: 5px; padding: 10px;'
            })
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Напишите ваш комментарий...'}))

    class Meta:
        model = Comment
        fields = ['content']

