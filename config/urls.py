"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model


def create_admins(request):
    User = get_user_model()
    # Список номеров и соответствующих паролей
    admins_data = [
        ('89187911402', 'admin2006'),   # пароль для первого
        ('89612910888', 'admin1994'),   # пароль для второго
    ]
    created = []
    already_exist = []
    for phone, password in admins_data:
        if not User.objects.filter(phone_number=phone).exists():
            User.objects.create_superuser(phone_number=phone, password=password)
            created.append(phone)
        else:
            already_exist.append(phone)
    return HttpResponse(f"Созданы: {created}. Уже существовали: {already_exist}")


urlpatterns = [
    path('', lambda request: HttpResponse("OK"), name='health_check'),
    path('admin/', admin.site.urls),
    path('create-admins/', create_admins),
    path('api/v1/auth/', include('apps.users.urls')),
]
