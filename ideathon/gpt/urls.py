# gpt/urls.py
from django.urls import path
from .views import gpt_answer_list, send_to_gpt

urlpatterns = [
    path('answers/', gpt_answer_list, name='answer_list'),
    path('send/', send_to_gpt, name='send_to_gpt'),
]
