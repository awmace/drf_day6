import jwt
from rest_framework import exceptions
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler


class JWTAuthentication(BaseJSONWebTokenAuthentication):

    def authenticate(self, request):

        # 获取前端传递的token：npf token zqy组合
        token = request.META.get("HTTP_AUTHORIZATION")
        print(token)

        # 自定义校验规则:判断是否是符合自定义的token封装,
        # 是的话返回token
        token = self.parse_jwt_token(token)

        if token is None:
            return None

        try:
            # 将发送过来token反解析出载荷
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed("签名已过期")
        except:
            raise exceptions.AuthenticationFailed("非法用户")

        # 如果没有任何错误  则将认证出的用户返回
        user = self.authenticate_credentials(payload)

        return user, token

    # 自定义token校验规则 npf token zqy
    def parse_jwt_token(self, jwt_token):
        tokens = jwt_token.split()
        if len(tokens) != 3 or tokens[0].lower() != "npf" or tokens[2].lower() != "zqy":
            return None

        return tokens[1]
