from . import views
from django.urls import path, include

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('create-teacher/', views.register_teacher, name='sign_up'),
    path('get_details/<int:class_id>', views.details, name='details'),
    path('get_topics/<int:class_id>', views.topic_details, name='topic_details'),
    path('enter-class/<int:class_id>', views.enter_class, name='enter_class'),
    path('inside-class/<int:class_id>/<int:record_id>', views.inside_class, name='inside'),
    path('exit-class/<int:class_id>', views.exit_class, name='exit_class'),
]
