from django.shortcuts import render
from .models import Item

#insert1
from django.http import HttpResponse

#select1
from .serializers import ItemSerializer
from rest_framework.renderers import JSONRenderer
import json 


# 127.0.0.1:8000/api/select1?key=abc&no=n
#{"id":"a"}
def select1(request):
    key = request.GET.get("key","")
    no = request.GET.get("no","1")
    search = request.GET.get("search","1")

    if (key == 'abc') and (no=='1'):
        
        obj = Item.objects.filter(name__contains='휴')[0:3]
        
        serializer = ItemSerializer(obj, many = True)
        print(serializer.data)
        data = JSONRenderer().render(serializer.data)
        return HttpResponse(data)
    
    
    #DB에서 확인 

    else : 
        data2 = json.dumps({"ret":'key error'})
        return HttpResponse(data2)
    
    

    # if key == 'abc' :        
    #     obj = Item.objects.get(no=no)
    #     serializer = ItemSerializer(obj)
    #     print(serializer.data)
    #     data = JSONRenderer().render(serializer.data)
    
    #return HttpResponse(data)


#[{"id":"a"},{"id":"b"}] 
def select2(request):
    obj = Item.objects.all()
    serializer = ItemSerializer(obj, many=True)
    data = JSONRenderer().render(serializer.data)
    return HttpResponse(data)


def insert1(request):   
    for i in range(1, 31, 1):
        obj = Item()
        obj.name = '휴대폰'+str(i)
        obj.price = 1000+i 
        obj.save()
    return HttpResponse("insert1")


