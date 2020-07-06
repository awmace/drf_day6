import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.settings import api_settings

from api.models import User

# 通过user对象生成载荷与通过载荷签发token
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserModelSerializer(ModelSerializer):
    # 自定义反序列化字段 代表这个字段只参与反序列化  且不会要求这个字段必须与model类映射
    account = serializers.CharField(write_only=True)
    passwords = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["account", "passwords", "username", "phone", "email"]

        # 只参与序列化的字段
        extra_kwargs = {
            "username": {
                "read_only": True,
            },
            "phone": {
                "read_only": True,
            },
            "email": {
                "read_only": True,
            }

        }

    def validate_account(self, value):
        return value

    def validate_passwords(self, value):
        return value

    def validate(self, attrs):
        account = attrs.get("account")
        passwords = attrs.get("passwords")

        # 依次是邮箱判断(a@b形式),手机号判断(1[3,9][0,9]*9位),用户名判断
        if re.match(r'.+@.+', account):
            user_obj = User.objects.filter(email=account).first()
        elif re.match(r'1[3-9][0-9]{9}', account):
            user_obj = User.objects.filter(phone=account).first()
        else:
            user_obj = User.objects.filter(username=account).first()

        # 判断用户是否存在 且用户密码是否正确：check_password():加密验证
        if user_obj and user_obj.check_password(passwords):
            # 生成载荷
            payload = jwt_payload_handler(user_obj)
            # 生成token
            token = jwt_encode_handler(payload)
            # 添加token和用户到attrs中用于返回给前端
            self.token = token
            self.obj = user_obj

        return attrs
