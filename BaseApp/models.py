from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=[('Non-elective', 'Non-elective'), ('Elective', 'Elective')])

    def __str__(self):
        return f'{self.name}'


class Teacher(AbstractUser):
    username = models.CharField(max_length=256, help_text='Please provide both names.')
    gender = models.CharField(max_length=10, choices=[('M', 'M'), ('F', 'F')], default='M')
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True, unique=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)
    is_class_tr = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'gender', 'phone']

    class Meta:
        unique_together = ['username']
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'

    def __str__(self):
        class_tr = 'Mr.' if self.gender == 'M' else 'Mrs.'
        return f"{class_tr} {self.username} "

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


# 12/09
class ClassCaptain(models.Model):
    username = models.CharField(max_length=250)
    gender = models.CharField(max_length=10, choices=[('M', 'M'), ('F', 'F')])
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'captain'
        verbose_name_plural = 'captains'

    def __str__(self):
        desc = 'Active' if self.status else 'Not Active'
        return f'{self.username} {desc}'


class ClassRoom(models.Model):
    name = models.CharField(max_length=100,
                            choices=[('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3'), ('S4', 'S4'), ('S5', 'S5'),
                                     ('S6', 'S6')])
    stream = models.CharField(max_length=10, choices=[('S', 'S'), ('H', 'H')])
    class_captain = models.ForeignKey(to=ClassCaptain, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='class_captain')
    state = models.BooleanField(default=False)
    current_teacher = models.ForeignKey(to=Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='current_teacher')
    class_teacher = models.ForeignKey(to=Teacher, null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='class_teacher')
    teachers = models.ManyToManyField(Teacher, related_query_name='teachers_for_class', )
    boys = models.IntegerField(default=0)
    girls = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} {self.stream}'


class Topic(models.Model):
    topic = models.CharField(max_length=400)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False, blank=False)
    class_name = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.class_name.name}  {self.topic}'


class ClassRecord(models.Model):
    week = models.CharField(max_length=10)
    date = models.DateField()
    day = models.CharField(max_length=20)
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_taught = models.ForeignKey(Subject, on_delete=models.CASCADE, related_query_name='subject_taught',
                                       help_text='Subject to be taught')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_query_name='topic_taught',
                              help_text='Topic to be taught')
    enter_time = models.TimeField(verbose_name='enter_time')
    exit_time = models.TimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    class_monitor = models.ForeignKey(ClassCaptain, on_delete=models.CASCADE, related_name='class_monitor')
    auto_removed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.week}--{self.teacher_name.username} {self.subject_taught}'

    # class Meta:
    #     ordering = ('-enter_time',)
