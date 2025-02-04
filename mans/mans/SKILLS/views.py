from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from .forms import RegisterForm
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import User, CourseEnrollment, Course, Module, Comment, Lesson
from .forms import CommentForm
from django.contrib.auth import logout



def main(request):
    return render(request, 'main.html')


def main2(request):
    return render(request, 'main2.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)  # Опционально - автоматический вход после регистрации
            return redirect('main')  # Перенаправление на главную страницу после успешной регистрации
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Проверка пользователя
            User = get_user_model()
            user = None

            if "@" in username_or_email:
                user = User.objects.filter(email=username_or_email).first()
            else:
                user = User.objects.filter(username=username_or_email).first()

            if user and user.check_password(password):
                # Логиним пользователя
                login(request, user)
                return redirect('profile')  # Перенаправление на главную страницу
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправляем на страницу профиля после сохранения
    else:
        form = ProfileForm(instance=user)

    # Извлекаем записи на курсы, на которые записан пользователь
    enrolled_courses = Course.objects.filter(users=user)

    return render(request, 'profile.html', {
        'form': form,
        'user': user,
        'enrolled_courses': enrolled_courses,  # Передаем курсы в контекст
    })


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course=course).order_by('order')  # Получаем все модули курса
    return render(request, 'course_details.html', {'course': course, 'modules': modules})


def enroll_course(request, course_id):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, id=course_id)
        # Проверяем, записан ли пользователь уже на курс
        if not CourseEnrollment.objects.filter(user=request.user, course=course).exists():
            CourseEnrollment.objects.create(user=request.user, course=course)
        return redirect('course_details', course_id=course.id)
    return redirect('login')


def module_detail(request, module_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправляем на страницу входа, если пользователь не авторизован

    module = get_object_or_404(Module, pk=module_id)
    lesson = module.lessons.first()  # Получаем первый урок из модуля
    comments = Comment.objects.filter(course=module.course)
    next_module = Module.objects.filter(order__gt=module.order).first()


    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Создаем новый комментарий
            Comment.objects.create(
                user=request.user,
                course=module.course,
                content=form.cleaned_data['content']
            )
            return redirect('module_detail', module_id=module.id)
    else:
        form = CommentForm()

    return render(request, 'course_content.html', {
        'module': module,
        'lesson': lesson,
        'comments': comments,
        'form': form,
        'next_module': next_module,  # Передаем следующий модуль в контекст
    })


def logout_view(request):
    logout(request)
    return redirect('main')  # или redirect('/') для главной страницы


def my_courses(request):
    user_courses = Course.objects.filter(users=request.user)  # Курсы, на которые записан текущий пользователь
    return render(request, 'mycourses.html', {'user_courses': user_courses})
