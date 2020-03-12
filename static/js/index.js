$("#mytab a").click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });

$("#con a").click(function (e) {
    e.preventDefault();
    $(this).tab("show");
});

var tab_list = document.getElementById("con");
var lis = tab_list.querySelectorAll("li");
var items = document.querySelectorAll('.item');
for (var i=0; i<lis.length;i++){
    lis[i].setAttribute('index',i);
    lis[i].onclick = function () {
        var index = this.getAttribute('index');
        for (var i=0;i<items.length;i++){
            items[i].style.display = 'none';
        }
        items[index].style.display = 'block';
    }
}
// 时间戳
function numFormat(num) {
    return ('00' + num).substr(-2);
}
function timeFormat(timestamp){
    var datetime = new Date(timestamp * 1000);
    var year = datetime.getFullYear();
    var month = numFormat(datetime.getMonth() + 1);
    var day = numFormat(datetime.getDate());
    var hour = numFormat(datetime.getHours());
    var minute = numFormat(datetime.getMinutes());
    var second = numFormat(datetime.getSeconds());
    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}
//文字输入异步提交
$('#comment_form').submit(function () {
    // 判断是否为空
    $("#comment_error").text("");
    if(CKEDITOR.instances['id_text'].document.getBody().getText().trim()=='')
    {
         $("#comment_error").text("内容不能为空");
         return false;
    }
    //更新数据
    CKEDITOR.instances['id_text'].updateElement();
    //异步提交
    $.ajax({
        url:"/text_input/",
        type:'POST',
        data:$(this).serialize(),
        cache:false,
        success:function (data) {
            var robot_html = '<div class="robot">'+data['robot'][0]+'('+timeFormat(data['robot'][1])+'):'
                +'<br>'+data['robot'][2]+'</div>';
            var user_html = '<div class="user">'+data['user'][0]+'('+timeFormat(data['user'][1])+'):'+
                data['user'][2]+'</div>';
            var comment_html = robot_html + user_html;
            $("#comment_list").prepend(comment_html);
            //清空
           CKEDITOR.instances['id_text'].setData('');
        },
        error:function (xhr) {
            $("#comment_error").text("发生未知错误");
        }
    });
    return false;
});

//声纹识别
var voice = document.getElementById('voice');
var random_num = document.querySelector('.number');
voice.onclick = function () {
    var number = test();
    var text = "请说出以下六个随机数：";
    var num = '';
    for (var i=0;i<number.length;i++)
    {
        num = num + number[i] + ',';
    }
    random_num.value = num;
    text = text + num;
    $("#voice_tip").text(text);
};

//产生随机数
function test() {
    var arr = [];
    for (var i = 0; i < 6; i++) {
        var num = Math.random() * 9;
        num = parseInt(num, 10);
        arr.push(num);
    }
    return arr;
}
//语音识别异步提交
var speech_file = document.getElementById('speech_file');
$('#speech_input').submit(function () {
    $("#speech_error").text("");
    if (speech_file.value==''){
        $("#speech_error").text("上传文件不能为空");
        return false;
    }
    $.ajax({
        url: '/speech/',
        type: 'POST',
        cache: false,
        data: new FormData($('#speech_input')[0]),
        processData: false,
        contentType: false,
        success: function (data) {
            var robot_html = '<div class="robot">'+data['robot'][0]+'('+timeFormat(data['robot'][1])+'):'
                +'<br>'+data['robot'][2]+'</div>';
            var user_html = '<div class="user">'+data['user'][0]+'('+timeFormat(data['user'][1])+'):'
                +'<br>'+data['user'][2]+'</div>'+'<br>';
            var comment_html = robot_html + user_html;
            $("#comment_list").prepend(comment_html);
             //清空
            speech_file.value = '';
        },
        error:function (xhr) {
            $("#speech_error").text("发生未知错误");
        }
    });
     return false;
});
//声纹识别异步提交
var voice_file = document.getElementById('voice_file');
$('#voice_input').submit(function () {
    $("#voice_error").text("");
    if (voice_file.value==''){
        $("#voice_error").text("上传文件不能为空");
        return false;
    }
    $.ajax({
        url: '/voice/',
        type: 'POST',
        cache: false,
        data: new FormData($('#voice_input')[0]),
        processData: false,
        contentType: false,
        success: function (data) {
            if (data['robot'][2] == '对不起，声纹验证失败。'){
                var robot_html = '<div class="text-danger">'+data['robot'][0]+'('+timeFormat(data['robot'][1])+'):'
                +'<br>'+data['robot'][2]+'</div>'+'<br>';
            }
            else {
                var robot_html = '<div class="text-success">'+data['robot'][0]+'('+timeFormat(data['robot'][1])+'):'
               +'<br>'+data['robot'][2]+'</div>'+'<br>';
            }
            $("#comment_list").prepend(robot_html);
            //清空
            voice_file.value = '';
        },
        error:function (xhr) {
            $("#voice_error").text("发生未知错误");
        }
    });
     return false;
});
// 首页
var first = document.querySelector(".first");
var home_page = document.getElementById('home_page');
home_page.onclick=function () {
    first.submit();
};
//上传模型异步提交
var upload_file = document.querySelectorAll('.upload_file');
$('#upload_model').submit(function () {
    $("#upload_error").text("");

    if (upload_file[2].value==''){
        $("#upload_error").text("上传文件不能为空");
        return false;
    }
    $.ajax({
        url: '/upload_model/',
        type: 'POST',
        cache: false,
        data: new FormData($('#upload_model')[0]),
        processData: false,
        contentType: false,
        success: function (data) {
            if (data['robot'][2] == '对不起，文件上传失败。'){
                var robot_html = '<div class="text-danger">'+data['robot'][0]+'('+timeFormat(data['robot'][1])+'):'
                +'<br>'+data['robot'][2]+'</div>'+'<br>';
            }
            else {
                var robot_html = '<div class="text-success">'+data['robot'][0]+'('+timeFormat(data['robot'][1])+'):'
               +'<br>'+data['robot'][2]+'</div>'+'<br>';
            }
            $("#comment_list").prepend(robot_html);
            //清空
            for (var i=0;i<upload_file.length;i++){
                upload_file[i].value = '';
            }
        },
        error:function (xhr) {
            $("#upload_error").text("账号或密码错误");
             for (var i=0;i<upload_file.length;i++){
                upload_file[i].value = '';
            }
        }
    });
     return false;
});