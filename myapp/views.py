from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def hello(request):
    return HttpResponse("你爸爸！！")

# def Index(request):
#     return render(request, "index.html")

def index(request):     #HttpRequest
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        print(request.method)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'wcnnnd' and password == '123':
            return HttpResponse('登陆成功')
        else:
            return HttpResponse('登陆失败')
    return render(request, 'login.html')

    # print(request.GET)  #<QueryDict: {'username': ['wcnnnd'], 'password': ['123']}>
    # username = request.GET.get('username')
    # password = request.GET.get('password')
    # print(username, password)
    # if username == 'wcnnnd' and password == '123':
    #     return HttpResponse("登陆成功")
    # # elif (len(username) == 0 and len(password) == 0):
    # #     return HttpResponse("登陆失败")
    # else:
    #     return render(request, 'login.html')
