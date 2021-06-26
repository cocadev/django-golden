from django.contrib import admin
from django.urls import path
from orderangel import views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import ObtainJSONWebToken
from authentication.backends import CustomJWTSerializer

urlpatterns = [
    url(r'^$', views.home, name="home"),
    path('admin/', admin.site.urls),
    url(r'^api/stores/$', views.stores, name="stores_api"),
    path('api/orders/users/<int:user>/', views.orders, name="secure.users.order"),
    path('api/auth/login/',  ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer), name="secure.users.order"),
    url(r'^auth-jwt/', obtain_jwt_token),
    url(r'^auth-jwt-refresh/', refresh_jwt_token),
    url(r'^auth-jwt-verify/', verify_jwt_token)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
