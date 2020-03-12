"""
地址路由
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('index/', index),
    path('speech/', speech),
    path('text_input/', text_input),
    path('clear_comment/', clear_comment),
    path('voice/', voice),
    path('upload_model/', upload_model),
]