
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from student import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home page
    path('', views.home, name='home'),

    # Student registration
    path('register/', views.register, name='register'),

    # Student login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='student/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    # Student logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Student dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # AI Tutor
    path('ai-tutor/', views.ai_tutor, name='ai_tutor'),

    # Topic Explainer
    path('topic-explainer/', views.topic_explainer, name='topic_explainer'),
]
