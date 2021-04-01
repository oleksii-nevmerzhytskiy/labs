from json import loads

from sys import getsizeof
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView

from calculation.models import CalculateResponse, CalculateRequest
from calculation.serializers import CalculationResponseSerializer, CalculationRequestSerializer
from calculation.utils import Calculator


class HomePageView(TemplateView):
    template_name = "index.html"

"""
Клас, що описує точку доступа до API застосунку. Має наслідуватись від
APIView.
"""
class CalculationView(APIView):
    def post(self, request: HttpRequest):
        """
        Описує обробник POST запитів для даної точки доступу. Аналогічно можна визначити
        обробники і для інших HTTP методів.
        """
        # Десеріалізувати тіло запиту із JSON строки у словник. Зауважте, тут ми вже маємо
        # доступ до усього тіла запиту, тобто Django гарантує, що усе тіло буде повінстю зчитане
        # незалежно від розміру.
        if int(request.headers.get("Content-Length")) > 100:
            return Response(status=413)
        parsed_request = loads(request.body)
        # Створити клас-серіалізатор, що провалідує правильність заповнення полів об'єкту
        request_data_serializer = CalculationRequestSerializer(data=parsed_request)
        if not request_data_serializer.is_valid():
            # Якщо валідацію не пройдено - сповістити клієнта про неправильний формат запиту
            return Response(status=400)
        # Створити об'єкт, що описує дані запиту, із провалідованих даних
        request_data = CalculateRequest(**request_data_serializer.validated_data)
        # Використання даних запиту у бізнес-логіці
        calculation_result = Calculator.calculate(request_data.input_value)
        # Створити об'єкт, що описує дані відповіді на запит
        response_data = CalculateResponse(calculation_result)
        # Створити клас-серіалізатор, що підготує об'єкт з даними для відповіді до серіалізації
        response_data_serializer = CalculationResponseSerializer(response_data)
        # Створити об'єкт відповіді із даними
        response = Response(response_data_serializer.data)
        # Повернути відповідь. Коректна доставка гарантована фреймворком.
        request.logger.info(f'success: {calculation_result}')
        return response



