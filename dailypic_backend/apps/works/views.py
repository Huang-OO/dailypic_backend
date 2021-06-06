import json
from django.db.models import Count, Min
from django.http import JsonResponse
from django.views import View
from works.models import WorkImg, WorkCollection
import logging
logger = logging.getLogger('django')


class CreateWorks(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        first_category = data.get('first_category')
        second_category = data.get('second_category')
        user_id = data.get('user_id')
        url = data.get('url')
        describe = data.get('describe')

        if not all([first_category, second_category, user_id, url]):
            return JsonResponse({
                'code': 400,
                'errmsg': '参数不完整'
            })

        try:
            work = WorkImg.objects.create(**data)
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '数据库操作失败'
            })

        return JsonResponse({
            'code': 2000,
            'msg': 'ok'
        })

    def put(self, request):
        work_id = request.GET.get('work_id', 0)
        data = json.loads(request.body.decode())

        try:
            work_query = WorkImg.objects.get(id=work_id)
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '查询数据库失败'
            })

        if not work_query:
            return JsonResponse({
                'code': 400,
                'errmsg': '数据错误'
            })

        work_query.describe = data.get('describe')

        work_query.save()
        return JsonResponse({
            'code': 2000,
            'msg': 'ok'
        })


class HomeListView(View):
    def get(self, request):

        category = int(request.GET['category']) if request.GET['category'].isdigit() else 0
        try:
            work_count_queries = (WorkImg.objects
                                  .filter(first_category=category)
                                  .values('second_category')
                                  .annotate(total_count=Count('id'), min_id=Min('id'))
                                  .all())
            work_count_dict = {
                item.get('min_id'): item.get('total_count') for item in work_count_queries
            }

            work_info_queries = (WorkImg.objects
                                 .filter(id__in=list(work_count_dict.keys()))
                                 .all()
                                 )
            res_list = []
            for query in work_info_queries:
                res_list.append({
                    'id': query.id,
                    'url': query.url,
                    'second_category': query.second_category,
                    'total_count': work_count_dict.get(query.id)
                })
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '查询数据库失败'
            })
        return JsonResponse({
            'code': 2000,
            'res_list': res_list
        })


class DetailListView(View):
    def get(self, request, second_category):
        user_id = request.GET.get('user_id', 0)
        try:
            work_queries = (WorkImg.objects
                            .select_related('user')
                            .filter(second_category=second_category)
                            .order_by('create_time')
                            )
            collection_queries = (WorkCollection.objects
                                  .filter(user_id=user_id)
                                  .distinct()
                                  )
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': "查询数据库失败"
            })
        collection_work_dict = {}
        for query in collection_queries:
            collection_work_dict[query.work_id] = True
        detail_list = []
        for query in work_queries:
            detail_list.append({
                'id': query.id,
                'user_id': query.user.id,
                'user_name': query.user.username,
                'avatar': query.user.avatar,
                'url': query.url,
                'describe': query.describe,
                'collection': collection_work_dict.get(query.id, False)
            })

        return JsonResponse({
            'code': 2000,
            'detail_list': detail_list
        })


class CollectionView(View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({
                'code': 400,
                'errmsg': '请登录后操作'
            })
        try:
            work_queries = (WorkCollection.objects
                            .filter(user_id=user_id)
                            .select_related('work')
                            .order_by('create_time'))
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '查询数据库失败'
            })

        collection_list = []
        for query in work_queries:
            collection_list.append({
                'id': query.id,
                'url': query.work.url,
                'describe': query.work.describe,
                'user_name': query.work.user.username,
                'avatar': query.work.user.avatar,
                'work_id': query.work.id,
                'collection': True
            })

        return JsonResponse({
            'code': 2000,
            'collection_list': collection_list
        })

    def post(self, request):
        data = json.loads(request.body.decode())
        user_id = data.get('user_id')
        work_id = data.get('work_id')
        if not user_id:
            return JsonResponse({
                'code': 400,
                'errmsg': '请登录'
            })
        if not all([user_id, work_id]):
            return JsonResponse({
                'code': 400,
                'errmsg': '参数不完整'
            })
        try:
            WorkCollection.objects.create(**data)
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '查询数据库失败'
            })

        return JsonResponse({
            'code': 2000,
            'msg': '收藏成功'
        })

    def delete(self, request):
        data = json.loads(request.body.decode())
        user_id = data.get('user_id')
        work_id = data.get('work_id')
        if not all([user_id, work_id]):
            return JsonResponse({
                'code': 400,
                'errmsg': '参数不完整'
            })
        try:
            WorkCollection.objects.filter(work_id=work_id,
                                          user_id=user_id).delete()
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '数据库操作失败'
            })

        return JsonResponse({
            'code': 2000,
            'msg': 'ok'
        })
