from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token

from api import views

urlpatterns = [
    url("login/", ObtainJSONWebToken.as_view()),
    # obtain_jwt_token:等同于ObtainJSONWebToken.as_view()
    # 通过jwt获取token
    url("obt/", obtain_jwt_token),

    path("user/", views.UserDetailAPIView.as_view()),
    path("check/", views.LoginAPIView.as_view()),
]
