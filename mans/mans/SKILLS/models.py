# Расширение стандартной модели User для добавления дополнительных полей
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)  # Уникальное имя пользователя
    profile_image = models.ImageField(upload_to='media/avatar', blank=True, null=True)  # Аватар пользователя
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(unique=True, max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Уникальное имя для обратной связи
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Уникальное имя для обратной связи
        blank=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name',
                       'phone']  # Поля, которые требуются при создании суперпользователя

    def __str__(self):
        return self.username

    #class Meta:
       # managed = True
        #db_table = 'users'


# Модель курса
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media/course', blank=True, null=True)
    users = models.ManyToManyField(User, through='CourseEnrollment', related_name='courses')

    def __str__(self):
        return self.title

    #class Meta:
        #managed = True
        #db_table = 'course'


# Модель для отслеживания, какой пользователь записан на какой курс
class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} записан на {self.course}"

    #class Meta:
        #managed = True
        #db_table = 'enrollments'


# Модель модуля для курса (каждый курс может иметь несколько модулей)
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField()  # Порядок модулей

    class Meta:
        ordering = ['order']  # Сортировка модулей по порядку
        #managed = True
        #db_table = 'moduls'

    def __str__(self):
        return f"{self.course} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)  # Связь с модулем
    title = models.CharField(max_length=200)  # Название урока
    content = models.TextField()  # Содержание урока
    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True)  # Изображение для урока
    video = models.FileField(upload_to='lesson_videos/', blank=True, null=True)  # Видео для урока
    order = models.IntegerField()  # Порядок урока (для сортировки)

    def __str__(self):
        return f"Урок {self.order}: {self.title}"

    class Meta:
        ordering = ['order']

# Модель комментариев для контента курса и обсуждений
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user} к курсу {self.course}"

   # class Meta:
       # managed = True
       # db_table = 'comments'
