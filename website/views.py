import os
import re
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .speech_voiceprint.voice_to_text import voice2text
from .speech_voiceprint.robot_answer import sizhi_msg
from .speech_voiceprint.check_voice import check_voice
from .speech_voiceprint.silence import denoise
from .models import Comment
from .models import UserTable
from .forms import CommentForm
# Create your views here.
# 百度语音合成
from .set import APP_ID, API_KEY, SECRET_KEY
# 语音识别上传文件
from .set import speech_path
# 声音模型
from .set import model_path
# 声纹识别
from .set import voice_original, denoise_voice


def function_out(func):
    """
    装饰器
    :param func:
    :return:
    """
    def function_in(request):
        if request.method == 'GET':
            return index(request)
        else:
            return func(request)
    return function_in


def index(request):
    """
    首页
    :param request:
    :return:
    """
    context = {}
    comments = Comment.objects.all()
    context['comments'] = comments
    context['comment_form'] = CommentForm()

    return render(request, "website/index.html", context)


@function_out
def speech(request):
    """
    语音识别上传文件
    :param request:
    :return:
    """
    data = {}
    # 保存语音文件
    try:
        file_name = request.FILES["file"].name
        file_path = speech_path + file_name
        with open(file_path, 'wb') as f:
            for i in request.FILES["file"].chunks():
                f.write(i)
        # 语音转文字
        try:
            text = voice2text(APP_ID, API_KEY, SECRET_KEY, file_path)
            tip = ''
        except:
            text = ['']
            tip = '【语音文件识别失败】'

        # 移除文件
        os.remove(file_path)
    except:
        text = ['']
        tip = ''

    comment = Comment()
    comment.user = "您"
    comment.text = text[0] + tip
    comment.save()

    data['user'] = [comment.user, comment.comment_time.timestamp(), comment.text]
    # 把文字提交机器人
    return_msg = sizhi_msg(text[0])

    comment = Comment()
    comment.user = "robot"
    comment.text = return_msg
    comment.save()
    data['robot'] = [comment.user, comment.comment_time.timestamp(), comment.text]
    return JsonResponse(data)


@function_out
def text_input(request):
    """
    文字输入
    :param request:
    :return:
    """
    data = {}

    text = request.POST.get('text', '')
    # 去掉HTML标签
    text_html = re.compile(r'<[^>]+>', re.S)
    text_str = text_html.sub('', text)

    comment = Comment()
    comment.user = "您"
    comment.text = text
    comment.save()

    data['user'] = [comment.user, comment.comment_time.timestamp(), comment.text]

    return_msg = sizhi_msg(text_str)
    comment = Comment()
    comment.user = "robot"
    comment.text = return_msg
    comment.save()

    # 返回数据
    data['robot'] = [comment.user, comment.comment_time.timestamp(), comment.text]
    # 异步提交
    return JsonResponse(data)


@function_out
def clear_comment(request):
    """
    清除对话列表
    :param request:
    :return:
    """
    Comment.objects.all().delete()
    context = {}

    comments = Comment.objects.all()
    context['comments'] = comments
    context['comment_form'] = CommentForm()

    return render(request, "website/index.html", context)


@function_out
def voice(request):
    """
    声纹识别
    :param request:
    :return:
    """
    data = {}
    models = os.listdir(model_path)
    if len(models) == 0:
        comment = Comment()
        comment.user = "robot"
        comment.text = "没有声学模型，无法进行声纹验证。"
        comment.save()

        data['robot'] = [comment.user, comment.comment_time.timestamp(), comment.text]

        return JsonResponse(data)
    try:
        file_name = request.FILES["file"].name
        number = request.POST.get('number', '')
        number = number[0::2]

        file_path = voice_original + file_name
        denoise_path = denoise_voice
        with open(file_path, 'wb') as f:
            for i in request.FILES["file"].chunks():
                f.write(i)
        # 声音降噪
        denoise(file_path, denoise_path + file_name)

        try:
            text = voice2text(APP_ID, API_KEY, SECRET_KEY, denoise_path + file_name)
        except:
            text = ['']
        # 声纹验证
        n = check_voice(denoise_path, model_path)
        # 移除文件
        os.remove(file_path)
        os.remove(denoise_path + file_name)
    except:
        n = 0
        number = ''
        text = ['']

    comment = Comment()
    comment.user = "robot"

    if n == 1 and number == text[0]:
        comment.text = "恭喜您，声纹验证通过。"
    else:
        comment.text = "对不起，声纹验证失败。"
    comment.save()

    data['robot'] = [comment.user, comment.comment_time.timestamp(), comment.text]

    return JsonResponse(data)


@function_out
def upload_model(request):
    """
    上传模型
    :param request:
    :return:
    """
    data = {}
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    username = get_object_or_404(UserTable.objects.filter(username=username))

    comment = Comment()
    comment.user = "robot"
    if password == username.password:
        try:
            file_name = request.FILES["file"].name
            file_path = model_path + file_name
            with open(file_path, 'wb') as f:
                for i in request.FILES["file"].chunks():
                    f.write(i)
            comment.text = "文件上传成功。"
        except:
            comment.text = "对不起，文件上传失败。"
    else:
        comment.text = "对不起，文件上传失败。"
    comment.save()

    data['robot'] = [comment.user, comment.comment_time.timestamp(), comment.text]

    return JsonResponse(data)