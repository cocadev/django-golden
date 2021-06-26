"""orderangel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from authentication import views
from django.conf.urls import url

urlpatterns = [
    # auth
    url(r'^login/$', views.login, name="login"),
    url(r'^auth/$', views.auth_view, name="auth"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^public/logout/$', views.public_logout, name="public-logout"),
    url(r'^pub-auth/$', views.public_auth, name="public-auth"),
    url(r'^register/$', views.register_user, name="register"),
    url(r'^register_success/$', views.register_success, name="register_success"),
]



