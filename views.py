import datetime
import json
import os

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render ,redirect
from django.urls import reverse

from ehrms.EmailBackEnd import EmailBackEnd
from ehrms.models import CustomUser,HR,adminnav,Employs,project_drop,admin_home_drop,admin_drop
from worktride import settings

from django.shortcuts import render, redirect
from django.contrib import messages
import requests,random
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Companys

def showDemoPage(request):
    return render(request,"demo.html")

def ShowLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # captcha_token=request.POST.get("g-recaptcha-response")
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        # cap_data={"secret":cap_secret,"response":captcha_token}
        # cap_server_response=requests.post(url=cap_url,data=cap_data)
        # cap_json=json.loads(cap_server_response.text)

        # if cap_json['success']==False:
        #     messages.error(request,"Invalid Captcha Try Again")
        #     return HttpResponseRedirect("/")

        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        
        if user is not None:
            request.session['email_2']=user.email;
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            
            else:
                return HttpResponseRedirect(reverse("Employ_home"))
        else:
            messages.error(request,"Invalid Username or Password")
            return HttpResponseRedirect("/show_login")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")

def Testurl(request):
    return HttpResponse("Ok")

def signup_admin(request):
    return render(request,"signup_admin_page.html")



def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    # try:
    user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
    user.email=email
    user.save()
    messages.success(request,"Successfully Created Admin")
    return HttpResponseRedirect(reverse("show_login"))
    # except:
    #     messages.error(request,"Failed to Create Admin")
    #     return HttpResponseRedirect(reverse("show_login"))
def signup_employ(request):
    return render(request,"registration/signup_employ_page.html")


def do_employ_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.save()
        messages.success(request,"Successfully Created Employ")
        return HttpResponseRedirect(reverse("signup_employ"))
    except:
        messages.error(request,"Failed to Create employ")
        return HttpResponseRedirect(reverse("signup_employ"))

def nav(request):
    return render(request,"nav.html")


def homepage(request):
    return render(request,"index.html")
    

def employeemonitoring(request):
    return render(request,"employee.html")

def timeattendance(request):
    return render(request,"attendance.html")

def activitymonitoring(request):
    return render(request,"activity.html")

def screenmonitoring(request):
    return render(request,"screen.html")


def productivity(request):
    return render(request,"product.html")


def timetracking(request):  
    return render(request,"time.html")

def officework(request):
    return render(request,"office.html")

def projectmanagment(request):
    return render(request,"project.html")



def features(request):
    return render(request,"features.html")


from .models import AdminHod


def admin_Password(request):
    admin = AdminHod.objects.get(admin=request.user.id) 

    user = CustomUser.objects.filter(id=request.user.id).first()
    userid1 = user.id
    da1 = AdminHod.objects.filter(admin=request.user.id).first()
    da2 = da1.id
    admin = AdminHod.objects.get(id=1)
    s = adminnav.objects.all()
    # projectm = admin_project_create.objects.filter(admin_id=userid1)
    h = HR.objects.all()
    employs_all = Employs.objects.all()
    admin_drops=admin_drop.objects.filter(parent_category=None).order_by('id')
    admin_home_drops=admin_home_drop.objects.filter(parent_category=None).order_by('id')
    data = AdminHod.objects.filter(id=request.user.id)
    projects_drops=project_drop.objects.filter(parent_category=None).order_by('id')

 

    return render(request,"admin-template/admin_Password.html", {'admin': admin,'user':user,'da1':da1,'da2':da2,'admin':admin,'admin_home_drops':admin_home_drops,'s':s,'h':h,'projects_drops':projects_drops,'data':data,'employs_all':employs_all,'admin_drops':admin_drops})







def admin_Password_save(request):
    # admin = AdminHod.objects.get(admin=request.user.id), {'admin': admin} 

    if request.method =="POST":
        password=request.POST.get("password")

        
        customuser=CustomUser.objects.get(id=request.user.id)
        if password!=None and password!="":
            customuser.set_password(password)
            customuser.save()

            employ=AdminHod.objects.get(admin=customuser)
            employ.save()
            return redirect('/admin_home')

    return render(request, "admin-template/admin_Password.html")




from django.shortcuts import render, redirect
from .models import Companys
from django.contrib import messages
import requests,random
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotAllowed


def send_msg(number, message, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    api = "AQk4vziURB67Nsiq0fI6yad28gHMC6snwacnN0ZW5EDFr4lyuuYREzTGyJ8a"
    querystring = {"authorization": api, "sender_id": "TEERDHA", "message": message, "language": "english", "route": "otp", "numbers": number, "variables_values": otp, "flash": "0"}
    headers = {'cache-control': "no-cache"}
    return requests.get(url, headers=headers, params=querystring)

def store_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        request.session['phone_number'] = phone_number
        response_data = {'success': True}
        return JsonResponse(response_data)

def send_otp(request):
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')

        if phone_number:
            otp = random.randint(1000, 9999)
            request.session['generated_otp'] = otp

            response = send_msg(phone_number, "Your OTP is: {}".format(otp), otp)

            if response.status_code == 200:
                response_data = {'success': True}
            else:
                response_data = {'success': False, 'error': 'Failed to send OTP via SMS.'}
        else:
            response_data = {'success': False, 'error': 'Phone number not found in session.'}

        return JsonResponse(response_data)

    # Return a 405 Method Not Allowed response for GET requests
    return HttpResponseNotAllowed(['POST'])

def verify_otp(request):
    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp')
        generated_otp = request.session.get('generated_otp', '')

        if user_entered_otp == str(generated_otp):
            response_data = {'message': 'OTP is valid.'}
        else:
            response_data = {'message': 'Invalid OTP. Please try again.'}

        return JsonResponse(response_data)



from django.contrib.auth import get_user_model

def register_company(request):
    if request.method == 'POST':
        organizationname = request.POST.get('organizationname')
        registration_number = request.POST.get('registration_number')
        address = request.POST.get('address')
        contact_person = request.POST.get('contact_person')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        Numberofemployees = request.POST.get('Numberofemployees')
        your_title = request.POST.get('your_title')
        user_entered_otp = request.POST.get("otp")
        generated_otp = request.session.get('generated_otp', '')

        # Verify OTP
        if user_entered_otp == str(generated_otp):
                user = CustomUser.objects.create_customuser(username=contact_person, password=password, email=email)
                comp=Companys.objects.get(usernumber=user)
                comp.organizationname=organizationname,
                comp.registration_number=registration_number,
                comp.address=address,
                comp.contact_person=contact_person,
                comp.email=email,
                comp.phone_number=phone_number,
                comp.password=password,
                comp.Numberofemployees=Numberofemployees,
                comp.your_title=your_title,
                comp.otp=user_entered_otp
                comp.save()
                messages.success(request, "WAIT FOR 4 - 8 HOURS ")
                del request.session['generated_otp']
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'admin-template/company_register.html')
    return render(request, 'admin-template/company_register.html')


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import admin_drop

def admincontrol(request):
    if request.method == 'POST':
        try:
            instances = admin_drop.objects.all()

            for instance in instances:
                show_key = f'show_{instance.id}'
                instance_id = int(request.POST.get(f'subid_{instance.id}', 0))

                if show_key in request.POST:
                    instance.show = int(request.POST[show_key])
                else:
                    instance.show = 1

                instance.save()
            return redirect('admincontrol')
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    # Fetch instances to display in the template initially
    instances = admin_drop.objects.all()
    context = {'shou': instances}
    return render(request, 'admincontrol.html', context)


