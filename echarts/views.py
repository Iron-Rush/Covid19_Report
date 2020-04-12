from django.shortcuts import render
from myapp.models import AllInfo, MXInfo
import datetime
# Create your views here.
def Index(request):
    all_info = AllInfo.objects.all()
    province_list = MXInfo.objects.values('province')
    # print(province_list)
    # print(all_info) #<QuerySet [<AllInfo: 2020-03-31 14:56:06+00:00>, <AllInfo: 2020-04-01 14:58:59+00:00>, <AllInfo: 2020-04-02 14:59:20+00:00>]>
    # print(type(all_info))   # <class 'django.db.models.query.QuerySet'>
    time_list = []
    confirm_list = []
    dead_list = []
    heal_list = []
    province_set = set()
    for province in province_list:
        province_set.add(province.get('province'))
    print(province_set)
    for info in all_info:
        time_info = datetime.datetime.strftime(info.time_info, "%Y-%m-%d")
        time_list.append(time_info)
        # print(time_info)
        confirm_list.append(info.confirm)
        dead_list.append(info.dead)
        heal_list.append(info.heal)
    return render(request, "index.html", {
        'time_list': time_list,
        'confirm_list': confirm_list,
        'dead_list': dead_list,
        'heal_list': heal_list,
        'province_set': province_set})

def MX(request, province):
    mx_info = MXInfo.objects.filter(province=province)
    name_list = []
    confirm_list = []
    suspect_list = []
    dead_list = []
    heal_list = []
    for info in mx_info:
        name_list.append(info.name)
        confirm_list.append(info.confirm)
        suspect_list.append(info.suspect)
        dead_list.append(info.dead)
        heal_list.append(info.heal)
    # print(mx_info)
    return render(request, "mx.html", {
        "name_list": name_list,
        "confirm_list": confirm_list,
        "suspect_list": suspect_list,
        "dead_list": dead_list,
        "heal_list": heal_list
    })