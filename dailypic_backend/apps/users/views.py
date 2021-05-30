from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection
from users.models import User
import re
import json
import logging
logger = logging.getLogger('django')
from django.contrib.auth import login, authenticate

# Create your views here.


class UsernameCountView(View):
    """判断用户名是否重复注册"""
    def get(self, request, username):
        """判断用户名是否重复"""
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': '访问数据库失败!'})

        return JsonResponse({
            'code': 2000,
            'msg': 'ok',
            'count': count
        })


class MobileCountView(View):
    def get(self, request, mobile):
        """判断手机号是否重复注册"""
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '查询数据库失败!'
            })
        return JsonResponse({
            'code': 2000,
            'msg': 'ok',
            'count': count
        })


class RegisterView(View):
    def post(self, request):
        """接受参数, 保存到数据库"""
        # 1. 接受参数
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('check_password')
        mobile = data.get('mobile')
        allow = data.get('checked')
        sms_code_client = data.get('mobile_code')

        # 2. 校验
        if not all([username, password, password2, mobile, allow, sms_code_client]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        # 3. username 校验
        if not re.match(r'^[a-zA-Z0-9]{3,20}$', username):
            return JsonResponse({
                'code': 400,
                'errmsg': 'username格式有误'
            })

        # 4. password 校验
        if not re.match(r'^.*(?=.{6,})(?=.*\d)(?=.*[A-Za-z]).*$', password):
            return JsonResponse({
                'code': 400,
                'errmsg': 'password格式有误'
            })

        # 5. password2 与 password是否一致
        if password != password2:
            return JsonResponse({
                'code': 400,
                'errmsg': '两次输入密码不一致'
            })

        # 6. 校验mobile
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': 'mobile格式有误'
            })

        # 7. allow 校验
        if allow is not True:
            return JsonResponse({
                'code': 400,
                'errmsg': '请同意'
            })

        # 8. sms_code 校验
        redis_conn = get_redis_connection('verify_code')

        # 9. 从redis中取值
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        # 10. 判断该值是否存在
        if not sms_code_server:
            return JsonResponse({
                'code': 400,
                'errmsg': '短信验证码过期'
            })

        # 11 把redis中取得和前端的值对比
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({
                'code': 400,
                'errmsg': '验证码有误'
            })

        # 12. 保存到数据库(username password mobile)
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 40,
                'errmsg': '保存数据库错误'
            })

        # 13. 拼接json返回
        return JsonResponse({
            'code': 2000,
            'errmsg': 'ok'
        })


class LoginView(View):
    def post(self, request):
        """实现登录接口"""
        # 1.接受参数
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')

        # 2. 校验(整体 + 单个)
        if not all([username, password]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        # 3. 验证是否能够登录
        user = authenticate(username=username,
                            password=password)

        # 判断是否为空, 如果为空, 返回
        if user is None:
            return JsonResponse({
                'code': 400,
                'errmsg': '用户名或密码错误'
            })

        # 4. 状态保持
        login(request, user)

        # 5. 判断是否记住用户
        if remembered != True:
            # 7.如果没有记住: 关闭立即失效
            request.session.set_expiry(0)
        else:
            # 6. 如果记住: 设置两周有效期
            request.session.set_expiry(None)

        user_info = {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'mobile': user.mobile
        }

        return JsonResponse({
            'code': 2000,
            'user_info': user_info,
            'errmsg': 'ok'
        })

