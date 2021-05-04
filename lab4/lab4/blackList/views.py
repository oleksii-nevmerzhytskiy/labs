import logging
from json import dumps, loads
from django.forms.models import model_to_dict

import redis
from django.urls import path
from blackList.models import ContactModel
from .serializers import ContactSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import FormView, TemplateView
from .forms import NameForm

logger = logging.getLogger('django')
redis_access = redis.Redis('localhost', port=6379, db=15)

class ContactListPageView(TemplateView):
    template_name = "index.html"

class ContactPageView(FormView):
    template_name = "view.html"
    form_class = NameForm

"""
Клас, що описує точку доступа із можливістю виконання CRUD операцій над об'єктом
Усі методи (крім get_details) відповідають одноіменним HTTP методам і являються їх обробниками
"""
class ContactView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ORM коллекція
        self.queryset = ContactModel.objects.all()
        self.serializer_class = ContactSerializer

    """
    Приклад отримання запису із БД. Якщо запис є в кеші - дістаємо звідти, якщо ні, шукаємо у БД і поміщаємо у кеш.
    """
    def get(self, request: Request):
        id = request.query_params.get('id', None)
        if id is None:
            records = self.queryset.all()
            serializer = self.serializer_class(records, many=True)
            return Response(serializer.data)
        else:
            return self.get_details(id)

    """
    Приклад оновлення запису у БД. При цьому не забуваємо скинути кеш у редісі.
    """
    def post(self, request):
        data = loads(request.body)
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(status=400)
        model = ContactModel(**serializer.data)
        model.pk = serializer.data['id']
        model.save()
        redis_access.delete(model.pk)
        return Response(status=200)

    """
    Приклад створення запису у БД.
    """
    def put(self, request):
        data = loads(request.body)
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(status=400)
        ContactModel(**serializer.data).save()
        return Response(status=201)

    """
    Приклад видалення запису у БД. При цьому не забуваємо скинути кеш у редісі.
    """
    def delete(self, request):
        data = loads(request.body)
        self.queryset.get(pk=data['id']).delete()
        redis_access.delete(data['id'])
        return Response(status=200)

    """
    Допоміжний метод для отримання запису з урахуванням стану кешу
    """
    def get_details(self, pk):
        logger.info(f'[Contacts] getting record with id = {pk}')
        # спроба отримати запис з кешу
        cached = redis_access.get(pk)
        if cached:
            logger.info(f'[Contacts] got record with id = {pk} from redis')
            # запис є у кеші, дістаємо його звідти
            cached = loads(cached)
            return Response(cached)
        logger.info(f'[Contacts] had to query record with id = {pk} from db')
        # запис немає у кеші, дістаємо його з БД
        obj = None
        try:
            obj = self.queryset.get(id=pk)
        except ContactModel.DoesNotExist:
            pass

        if not obj:
            return Response(status=404)
        dict_obj = model_to_dict(obj)
        serializer = self.serializer_class(data=dict_obj)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=400)
        data = serializer.data
        # зберігаємо запис у кеш на майбутнє
        redis_access.set(pk, dumps(data), ex=780)
        return Response(data)

routes = [
    path('api/contacts/', ContactView.as_view()),
    path('', ContactListPageView.as_view()),
    path('view', ContactPageView.as_view()),
    path('new', ContactPageView.as_view())

]








