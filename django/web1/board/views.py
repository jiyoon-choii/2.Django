from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base64 import b64encode # b64encode
import pandas as pd 

from .models import Table1

from .models import Table2 #models.py파일의 Talbe2 클래스
# byte배열을 base64(포맷-이미지출력)로 변경함, 

cursor = connection.cursor() #sql로 수행하기 위한 cursor객체


def t2_update_all(request):
    if request.method == 'GET':
        n = request.session['no']
        print(n)
        rows = Table2.objects.filter(no__in=n)
        return render(request, 'board/t2_update_all.html', {"list":rows})

    elif request.method == 'POST' :    
        menu = request.POST['menu']
        if menu == '1':    
            no = request.POST.getlist("chk[]")
            request.session['no'] = no
            print(no)
            return redirect("/board/t2_update_all")
        elif menu == '2':
            no = request.POST.getlist("no[]")
            name = request.POST.getlist("name[]")
            kor = request.POST.getlist("kor[]")
            eng = request.POST.getlist("eng[]")
            math = request.POST.getlist("math[]")
            objs = []
            for i in range(0, len(no), 1):
                obj = Table2.objects.get(no=no[i])
                obj.name = name[i]
                obj.kor = kor[i]
                obj.eng = eng[i]
                obj.math = math[i]
                obj.append(obj)
            Table2.objects.bulk_update(objs, ["name","kor","eng","math"])

            return redirect("/board/t2_list")




def t2_insert_all(request):
    if request.method == 'GET':
        return render(request,'board/t2_insert_all.html', {"cnt":range(15)})

    elif request.method == 'POST' :
        na = request.POST.getlist('name[]')
        ko = request.POST.getlist('kor[]')
        en = request.POST.getlist('eng[]')
        ma = request.POST.getlist('math[]')

        objs = []

        for i in range(0, len(na), 1):
            obj = Table2()
            obj.name = na[i]
            obj.kor = ko[i]
            obj.eng = en[i]
            obj.math = ma[i]   
            objs.append(obj)
        
        #일괄 추가
        Table2.objects.bulk_create(objs)
        return redirect("/board/t2_list") 
        
@csrf_exempt 
def t2_update(request):
    if request.method == 'GET':
        n = request.GET.get("no",0)       
        #SQL : SELECT * FROM BOARD_TABLE2 WHERE NO=%s 
        row = Table2.objects.get(no=n)
        return render(request,'board/t2_update.html',{"one":row})
    elif request.method == 'POST' :
        n = request.POST['no']
        obj = Table2.objects.get(no=n) #obj객체 생성
        obj.name = request.POST['name'] #변수에 값
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.save() #저장하기 수행 
        # UPDATE BOARD_TABLE2 SET 
        # NAME=%s, KOR=%s, ENG=%s, MATH=%s
        # WHERE NO= %s
        return redirect("/board/t2_list") 


@csrf_exempt 
def t2_delete(request):
    if request.method == 'GET':
        n = request.GET.get("no",0)
       
        #SQL : SELECT * FROM BOARD_TABLE2 WHERE NO=%s 
        row = Table2.objects.get(no=n)

        row.delete()  #삭제

        return redirect("/board/t2_list")



@csrf_exempt 
def t2_list(request):
    if request.method == 'GET':
        rows = Table2.objects.all()
        print(rows)
        print (type(rows))
        return render(request, 'board/t2_list.html',{"list":rows})
        #html표시


@csrf_exempt 
def t2_insert(request):
    if request.method == 'GET':
        return render(request, 'board/t2_insert.html')
    elif request.method == 'POST' :
        obj = Table2() #obj객체 생성
        obj.name = request.POST['name'] #변수에 값
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.save() #저장하기 수행 

        return redirect("/board/t2_insert")

#################################################

def select(request):
    txt = request.GET.get("txt","")
    page = int(request.GET.get("page",1))
    
    if txt == "":
        list = Table1.objects.all()[page*10-10:page*10]

        cnt = Table1.objects.all().count()
        total = (cnt-1)//10+1

    else :
        list = Table2.objects.filter(name__contains=txt)[page*10-10:page*10]

        cnt = Table1.objects.filter(name__contains=txt).count()
        total = (cnt-1)//10+1 

    return render(request, 'board/select.html', {"list":list, "pages":range(1,total+1,1)})



def dataframe(request):
    if request.method == 'GET':
        df = pd.read_sql(  
            """
            SELECT NO, WRITER, HIT, REGDATE
            FROM BOARD_TABLE1
            """, con=connection)
        print(df)
        print(df['NO'])
        return render(request, 'board/dataframe.html', {"df":df.to_html(classes="table")} )

@csrf_exempt  
def edit(request):
    if request.method == 'GET':
        no = request.GET.get("no",0)
        
        sql = """
            SELECT NO, TITLE, CONTENT
            FROM BOARD_TABLE1
            WHERE NO=%s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()
        return render(request, 'board/edit.html',
            {"one":data})

    elif request.method == 'POST':
        no = request.POST['no']
        ti = request.POST['title']    
        co = request.POST['content']

        arr = [ti,co,no]
        sql = """
            UPDATE BOARD_TABLE1 SET TITLE=%s,
            CONTENT=%s WHERE NO =%s
        """
        cursor.execute(sql, arr)
        return redirect("/board/content?no="+no)            


# 127,0,0,1:8000/board/delete/
@csrf_exempt  
def delete(request):
    if request.method == 'GET':
        no = request.GET.get("no",0)
        sql = """
            DELETE FROM BOARD_TABLE1
            WHERE NO=%s
        """
        cursor.execute(sql, [no])
        return redirect("/board/list")


@csrf_exempt  
def content(request):
    if request.method == 'GET':
        no = request.GET.get('no', 0)
        if no == 0 : 
            return redirect("/board/list") 

        if request.session['hit'] == 1 :
            sql = """
                UPDATE BOARD_TABLE1 SET HIT=HIT+1   WHERE NO = %s
            """
            cursor.execute(sql,[no])
            request.session['hit'] = 0        
        
        # 이전글 번호 가져오기
        sql = """
        SELECT NVL(MAX(NO), 0)
        FROM BOARD_TABLE1
        WHERE NO < %s 
        """
        cursor.execute(sql, [no])
        prev = cursor.fetchone()

        # 다음글 번호 가져오기
        sql = """
        SELECT NVL(MIN(NO), 0)
        FROM BOARD_TABLE1
        WHERE NO > %s 
        """
        cursor.execute(sql, [no])
        next = cursor.fetchone()  #(8,)  a[0]
        

        #가져오기
        sql = """
            SELECT NO, TITLE, CONTENT, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS'),
            IMG
        FROM BOARD_TABLE1
        WHERE NO = %s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()
        print(data) # DB에서 받은 게시물 1개의 정보 출력 
        if data[6] : # 바이트배열을 img에 넣음
            img = data[6].read()
            img64 = b64encode(img).decode("utf-8") 
        else : # 없는 경우 
            file = open('static/img/default.png','rb')
            img = file.read()
            img64 = b64encode(img).decode("utf-8")
            

        #print(no)
        return render(request, 'board/content.html', {"one":data, "image":img64, "prev":prev[0], "next":next[0]}) 




@csrf_exempt  
def list(request):
    

    txt = request.GET.get("txt","")         #초기값
    page = int(request.GET.get("page", 1))

    if txt == "":
        abc = Table1.objects.all()[page*10-10:page*10] 

        cnt = Table1.objects.all().count()
        total = (cnt-1)//10+1 
    
    else :
        abc = Table1.objects.filter(name__contains=txt)[page*10-10:page*10] 

        cnt = Table1.objects.filter(name__contains=txt).count()
        total = (cnt-1)//10+1

    return render(request, 'board/list.html', 
            {"list":abc, "pages":range(1,total+1,1)}) 

    '''
        # sql = """
        #     SELECT NO, TITLE, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS')
        # FROM BOARD_TABLE1
        # ORDER BY NO DESC
        # """
        # cursor.execute(sql)
        data = Table1.objects.all()[page*10-10:page*10]
        
        print( type(data) )            #[(),()]
    '''
    
    
@csrf_exempt  
def write(request):
    if request.method == 'GET':
        return render(request, 'board/write.html') 
    elif request.method == "POST" :
        tmp = None
        if 'img' in request.FILES:
            img = request.FILES['img']
            tmp = img.read()

        
        arr = [
            request.POST['title'],
            request.POST['content'],
            request.POST['writer'],
            tmp
        ]

        try : 
            #print(arr)
            sql = """
                INSERT INTO BOARD_TABLE1(TITLE, CONTENT, WRITER, IMG,  HIT, REGDATE)
                VALUES(%s,%s,%s,%s, 19832, SYSDATE)
            """
            cursor.execute(sql, arr)
        except Exception as e:
            print(e)


        return redirect("/board/list") # <a href 와 같음 

