import json

from django.http import JsonResponse
from django.views import View
from topic.models import Topic
import logging
logger = logging.getLogger('django')


class TopicView(View):
    def post(self, request):
        data = json.loads(request.body.decode())

        text = data.get('text')

        try:
            Topic.objects.create(text=text)
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '查询数据库失败'
            })

        return JsonResponse({
            'code': 2000,
            'msg': 'ok'
        })

    def get(self, request):
        try:
            topic_queries = Topic.objects.filter().all()
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '查询数据库失败'
            })

        topic_list = []
        for query in topic_queries:
            topic_list.append({
                'id': query.id,
                'text': query.text
            })

        return JsonResponse({
            'code': 2000,
            'topic_list': topic_list
        })