import uuid
import logging
from django.http import JsonResponse
from django.views import View
from dailypic_backend.utils.fastdfs.fastdfs_storage import FastDFSStorage
logger = logging.getLogger('django')


class UploadImage(View):
    def post(self, request):
        try:
            file = request.FILES['file']
            fast_dfs_storage = FastDFSStorage()
            file_name = fast_dfs_storage.save(file.name, file)
            url = fast_dfs_storage.url(file_name)
            return JsonResponse({
                'code': 2000,
                'url': url
            })
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '上传图片失败!'
            })

    def get(self, request):
        return JsonResponse({
            'state': 'SUCCESS',
            'list': [],
            "start": 1,  # 为请求参数start，会根据滚动条变化，变化值为 start+=size
            "totle": 1
        })
