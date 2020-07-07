import re

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import jwt_encode_handler

from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

from api.authentication import JWTAuthentication
from api.filter import LimitFilter, ComputerFilterSet
from api.models import User, Computer
from api.paginations import NpfPageNumberPagination, NpfLimitPagination, NpfCoursePagination
from api.serializers import UserModelSerializer, ComputerModelSerializer
from utils.response import APIResponse
from rest_framework_jwt.settings import APISettings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class UserDetailAPIView(APIView):
    # 开启了认证和权限，登录后可访问，先发起post请求获取token
    permission_classes = [IsAuthenticated]
    # 默认的token校验
    # authentication_classes = [JSONWebTokenAuthentication]

    # 自定义的token校验
    authentication_classes = [JWTAuthentication]

    # 携带生成的token访问
    def get(self, request, *args, **kwargs):
        return APIResponse(results={"username": request.user.username})


class LoginAPIView(APIView):
    # 禁用权限与组件
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 账号:account(手机号|邮箱|用户名)  密码:passwords
        # 反序列化
        user_ser = UserModelSerializer(data=request.data)
        # 校验信息，错误则返回异常信息
        user_ser.is_valid(raise_exception=True)
        # 返回结果
        return APIResponse(
            data_message="ok",
            token=user_ser.token,
            results=UserModelSerializer(user_ser.obj).data)

    # 入职等同于离职的写法:简单但不严谨，维护成本高
    def demo_post(self, request, *args, **kwargs):
        account = request.data.get("account")
        passwords = request.data.get("passwords")

        if re.match(r'.+@.+', account):
            user_obj = User.objects.filter(email=account).first()
        elif re.match(r'1[3-9][0-9]{9}', account):
            user_obj = User.objects.filter(phone=account).first()
        else:
            user_obj = User.objects.filter(username=account).first()

        # 用户和密码判断
        if user_obj and user_obj.check_password(passwords):
            # 生成载荷信息
            payload = jwt_payload_handler(user_obj)
            # 生成token
            token = jwt_encode_handler(payload)
            return APIResponse(results={"username": user_obj.username}, token=token)

        return APIResponse(data_message="game over")


class ComputerListAPIView(ListAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerModelSerializer

    # 配置过滤器类：
    # (1)DjangoFilterBackend：精确查询  (2)LimitFilter：自定义简单分页
    # (3)SearchFilter:模糊查询          (4)OrderingFilter：排序
    filter_backends = [SearchFilter, OrderingFilter, LimitFilter,DjangoFilterBackend]
    # 指定当前搜索条件:模糊查询
    # 前端为url?search=a :查询name包含a的数据
    search_fields = ['name', 'price']  # 一一查询
    # 指定排序的条件
    # ordering = ["price"]

    # 指定分页器,不能用元组或列表，会报错,这里是基础分页器
    # pagination_class = NpfPageNumberPagination

    # 这里是偏移分页器
    # pagination_class = NpfLimitPagination

    # 这里是游标分页器
    # pagination_class = NpfCoursePagination

    # 查询价格大于5000  小于 7000  电脑
    # django-filter 查询   通过filter_class指定过滤器
    filter_class = ComputerFilterSet
