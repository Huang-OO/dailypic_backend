import base64
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection
import random
from dailypic_backend.libs.captcha.captcha import captcha
import logging
logger = logging.getLogger('django')
from dailypic_backend.libs.yuntongxun.ccp_sms import CCP

# Create your views here.


class ImageCodeView(View):
    """返回图形验证码的类视图"""

    def get(self, request, uuid):
        """
        生成图形验证码, 保存到redis中, 另外返回图片
        :param request: 请求对象
        :param uuid: 浏览器端生成的唯一id
        :return: 图片
        """
        # 1. 调用工具类captcha生成图片验证码
        text, image = captcha.generate_captcha()

        # 2. 连接redis, 获取连接对象
        redis_conn = get_redis_connection('verify_code')

        # 3.利用连接对象, 保存数据到redis, 使用setex函数
        # redis_conn.setex('<key>', '<expire>', '<value>')
        redis_conn.setex('img_%s' % uuid, 300, text)
        image = base64.b64encode(image)

        return JsonResponse({
            'code': 2000,
            'msg': image.decode()
        })


class SMSCodeView(View):
    """短信验证码"""
    def get(self, request, mobile):
        """

        :param request: 请求对象
        :param mobile: 手机号
        :return: Json
        """
        # 将这句话提到前面最开始的位置:
        redis_conn = get_redis_connection('verify_code')
        # 进入函数后, 先获取存在在redis中的数据
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        # 查看数据是否存在, 如果存在, 说明60s没过返回
        if send_flag:
            return JsonResponse({
                'code': 400,
                'errmsg': '发送短信过于频繁'
            })

        # 1. 接受参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        # 2. 校验参数
        if not all([image_code_client, uuid]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        # 3. 创建连接到redis的对象

        # 4. 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return JsonResponse({
                'code': 400,
                'errmsg': '图形验证码失效'
            })

        # 5. 删除图形验证码, 避免恶意测试图形验证码
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.info(e)

        # 6. 对比图形验证码
        # bytes 转为字符串
        image_code_server = image_code_server.decode()
        # 转小写后比较
        if image_code_client.lower() != image_code_server.lower():
            return JsonResponse({
                'code': 400,
                'errmsg': '输入得人图形验证码有误'
            })

        # 7. 生成短信验证码, 生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)

        # 创建Redis管道
        pl = redis_conn.pipeline()

        # 将Redis请求添加到队列
        # 8. 保存短信验证码
        # 短信验证码有效期, 单位: 300 秒
        pl.setex('sms_%s' % mobile,
                 300,
                 sms_code)

        # 往redis中写入一个数据, 写入什么不重要, 时间重要
        # 我们给写入的数据设置为60s, 如果过期, 则会获取不到
        pl.setex('send_flag_%s' % mobile, 60, 1)

        # 执行请求,
        pl.execute()

        # 9. 发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        print(sms_code)
        return JsonResponse({
            'code': 2000,
            'msg': '发送短信成功'
        })
