import hashlib
import os
from django.http import HttpResponse


def valid_user(username):
    filepath = os.getcwd() + '/Server/user/user_info/'
    # print(filepath)
    files = os.listdir(filepath)
    for fi in files:
        # fi_d = os.path.join(filepath, fi)
        if fi == username:
            return username
    return ''

def set_user(request):
    user_info = ['822e0a98cec0337b747366676ae098f5', '2567a5ec9705eb7ac2c984033e06189d']
    request.encoding = 'utf-8'
    if 'username' in request.GET and request.GET['username'] and 'password' in request.GET and request.GET['password']:
        username = request.GET['username'].strip()
        password = request.GET['password'].strip()

        # 已存在
        if valid_user(username) == username:
            return HttpResponse('user error')

        # 加密密码
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf8'))
        md5 = hl.hexdigest()

        # 加密账号
        hl2 = hashlib.md5()
        hl2.update(username.encode(encoding='utf8'))
        user_code = hl2.hexdigest()
        if user_code not in user_info:
            return HttpResponse('no permission')

        with open(os.getcwd() + '/Server/user/user_info/' + username, 'w')as f:
            f.write(md5)

        return HttpResponse('username: ' + username + '<br>' + 'password: ' + password)
    else:
        return HttpResponse('error')
