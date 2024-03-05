from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
from utils import my_days
from . import forms
from . import models


# Create your views here.
@login_required(login_url='/login')
def home(request):
    user_id = request.user.id
    user = models.Teacher.objects.get(id=user_id)
    if user.is_teacher:
        classes = models.ClassRoom.objects.all()
        inside = [side_class for side_class in classes if side_class.current_teacher == user]
        if not inside:
            page = 'enter'
            teacher_classes = models.ClassRoom.objects.filter(teachers=user).distinct()
            available_classes = [class_object for class_object in teacher_classes if not class_object.state]
            context = {'available_classes': available_classes, 'page': page}
            return render(request, 'BaseApp/home.html', context)
        else:
            page = 'inside'
            entered_class = inside[0]
            record = models.ClassRecord.objects.filter(teacher_name=user, class_monitor=entered_class.class_captain,
                                                       exit_time__isnull=True).first()
            time_in = record.enter_time
            duration = datetime.datetime.combine(record.date, time_in)
            subject = record.subject_taught
            topic = record.topic
            boys = entered_class.boys
            girls = entered_class.girls
            population = boys + girls
            context = {'page': page, 'boys': boys, "entered_class": entered_class, 'girls': girls,
                       "population": population,
                       'enter_time': time_in, 'subject': subject, 'topic': topic, 'duration': duration}
            return render(request, 'BaseApp/inside.html', context)
    else:
        return render(request, 'BaseApp/errors.html')


def register_teacher(request):
    if request.method == 'POST':
        form = forms.RegisterTeacher(data=request.POST)
        if form.is_valid():
            user = form.save()
            authenticate(user)
            login(request, user)
            messages.info(request, 'Account Created')
            return redirect('base:home')
        messages.error(request, 'Error Occurred')
    else:
        form = forms.RegisterTeacher()

    context = {'form': form}
    return render(request, 'BaseApp/create_teacher.html', context)


@login_required(login_url='/login')
def details(request, class_id):
    page = 'one'
    teacher = models.Teacher.objects.get(id=request.user.id)
    subjects = teacher.subjects.all()
    context = {'subjects': subjects, 'page': page, 'class_id': class_id}

    return render(request, 'BaseApp/forms.html', context)


@login_required()
def topic_details(request, class_id):
    if request.method == 'POST':
        try:
            page = 'two'
            subject_id = int(request.POST['subject_taught'])
            subject = models.Subject.objects.get(id=subject_id)
            class_name = models.ClassRoom.objects.get(id=class_id)
            topics = models.Topic.objects.filter(subject=subject, class_name__name=class_name.name)
            print(topics)
            context = {'subject_taught': subject_id, 'page': page, 'class_id': class_id, 'topics': topics}
            return render(request, 'BaseApp/forms.html', context)
        except ValueError:
            page = 'one'
            teacher = models.Teacher.objects.get(id=request.user.id)
            subjects = teacher.subjects.all()
            context = {'subjects': subjects, 'page': page, 'class_id': class_id}

            return render(request, 'BaseApp/forms.html', context)
    else:
        page = 'one'
        teacher = models.Teacher.objects.get(id=request.user.id)
        subjects = teacher.subjects.all()
        context = {'subjects': subjects, 'page': page, 'class_id': class_id}

        return render(request, 'BaseApp/forms.html', context)


@login_required(login_url='/login')
def enter_class(request, class_id):
    if request.method == 'POST':
        try:
            current_teacher = models.Teacher.objects.get(id=request.user.id)
            subject_id = int(request.POST['subject_taught'])
            subject = models.Subject.objects.get(id=subject_id)
            class_name = models.ClassRoom.objects.get(id=class_id)
            topic, created = models.Topic.objects.get_or_create(topic=request.POST['topic'], subject=subject,
                                                                class_name=class_name)
            if not class_name.state:
                class_name.state = True
                class_name.current_teacher = current_teacher
                class_name.save()
            else:
                messages.info(request, 'Some One is inside the class')
                return redirect('base:home')

            today = datetime.datetime.today()
            new_record = models.ClassRecord()
            new_record.week = 'Week 1'
            new_record.date = datetime.datetime.today().date()
            new_record.day = my_days[today.weekday()]
            new_record.teacher_name = current_teacher
            new_record.subject_taught = subject
            new_record.topic = topic
            new_record.enter_time = today.time()
            new_record.class_monitor = class_name.class_captain
            if class_name.teachers.filter(username=current_teacher.username).first():
                new_record.save()
            else:
                messages.info(request, f'You can\'t enter {class_name}. Because you dont teach it')
                return redirect('base:home')

            record_id = new_record.id
            messages.info(request, f'You have entered {class_name}. Have a nice lesson')
            return redirect('base:inside', class_id, record_id)

        except ValueError:
            messages.error(request, 'Please Select a Subject')
            teacher = models.Teacher.objects.get(id=request.user.id)
            subjects = teacher.subjects.all()
            topics = models.Topic.objects.filter(class_name=class_id)

            context = {'subjects': subjects, 'topics': topics, 'class_id': class_id}

            return render(request, 'BaseApp/forms.html', context)

    else:
        teacher = models.Teacher.objects.get(id=request.user.id)
        subjects = teacher.subjects.all()
        topics = models.Topic.objects.filter(class_name=class_id)

        context = {'subjects': subjects, 'topics': topics}

        return render(request, 'BaseApp/forms.html', context)


@login_required(login_url='/login')
def inside_class(request, class_id, record_id):
    page = 'inside'
    entered_class = models.ClassRoom.objects.get(id=class_id)
    new_record = models.ClassRecord.objects.filter(id=record_id).first()
    if new_record is None:
        messages.info(request, 'Such a record does not exist')
        return redirect('base:home')
    else:
        time_in = new_record.enter_time.strftime('%H:%M')
        duration = datetime.datetime.combine(new_record.date, new_record.enter_time)
        subject = new_record.subject_taught
        topic = new_record.topic
        boys = entered_class.boys
        girls = entered_class.girls
        population = boys + girls
        context = {'page': page, 'boys': boys, "entered_class": entered_class, 'girls': girls,
                   "population": population,
                   'enter_time': time_in, 'subject': subject, 'topic': topic, 'duration': duration}

        if request.user.id == new_record.teacher_name.id:
            return render(request, 'BaseApp/inside.html', context)
        else:
            messages.warning(request, 'you are trying to see the current state of a class you never entered')
            return redirect('base:home')


@login_required(login_url='/login')
def exit_class(request, class_id):
    # resetting the class

    user_id = request.user.id
    user = models.Teacher.objects.get(id=user_id)
    wanted_class = models.ClassRoom.objects.get(id=class_id)
    if wanted_class.current_teacher.id == request.user.id:
        current_tr = None
        wanted_class.state = False
        wanted_class.current_teacher = current_tr
        wanted_class.save()
    else:
        messages.warning(request, 'You are trying to exit a class you never entered')
        return redirect('base:home')

    record = models.ClassRecord.objects.filter(teacher_name=user, class_monitor=wanted_class.class_captain,
                                               exit_time__isnull=True).first()
    today = datetime.datetime.today()
    now = today.time()
    record.exit_time = now
    if record.teacher_name.id == request.user.id:
        record.save()
    else:
        messages.info(request, 'You are trying to edit records you did not keep')
        return redirect('base:home')
    duration = datetime.datetime.combine(today.date(), record.exit_time) - datetime.datetime.combine(
        today.date(), record.enter_time)
    minutes = duration.total_seconds() / 60
    rounded_minutes = round(minutes, 2)
    record.duration = rounded_minutes
    if record.teacher_name.id == request.user.id:
        record.save()
    else:
        return redirect('base:home')
    messages.info(request, f'You have left {wanted_class}. Thank you for your service')

    return redirect('base:home')
