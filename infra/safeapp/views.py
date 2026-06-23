import time
from .emergency_ai import detect_emergency
from django.shortcuts import render
from .models import Notification, Report, User, Compensation
import bcrypt
from .ai import detect_issue

# Create your views here.
from django.shortcuts import render, redirect
from .models import Report, User
import bcrypt
from .ai import detect_issue
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')  

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        User(
            name=name,
            email=email,
            password=hashed.decode(),
            role=role 
        ).save()

        return redirect('/')

    return render(request, 'register.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')   # 👈 important

        user = User.objects(email=email).first()
        if not user:
            print("❌ User not found")
            return render(request, 'index.html', {'error': 'User not found'})

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            print("❌ Wrong password")
            return render(request, 'index.html', {'error': 'Wrong password'})

        if user.role != role:
            print("❌ Role mismatch")
            return render(request, 'index.html', {'error': 'Wrong role'})

        print("✅ Login success")

        if user and bcrypt.checkpw(password.encode(), user.password.encode()):

            # ✅ check role
            if user.role != role:
                return render(request, 'index.html', {'error': 'Wrong role selected'})

            request.session['user'] = email
            request.session['role'] = role

            # 🔥 redirect based on role
            if role == 'admin':
                return redirect('/admin_dashboard/')
            else:
                return redirect('/dashboard/')
        return render(request, 'index.html', {'error': 'Invalid credentials'})
            


def admin_dashboard(request):
    if request.session.get('role') != 'admin':
        return redirect('/')   # 🔒 block unauthorized access

   
    notification = Notification.objects(
        is_read=False
    ).first()
    if notification:
        notification.is_read = True
        notification.save()

    all_reports = Report.objects(
        ai_result__ne="Invalid Report"
    )

    emergency_reports = []
    normal_reports = []

    for report in all_reports:
        if report.description == "SOS Emergency":
            emergency_reports.append(report)
        else:
            normal_reports.append(report)

    users_data = []

    all_users = User.objects(email__ne="admin@gmail.com")

    for user in all_users:

        reports_count = Report.objects(
            user_email=user.email
        ).count()

        compensations = Compensation.objects(
            victim_email=user.email
        )

        total_comp = 0

        for comp in compensations:
            total_comp += comp.amount

        users_data.append({
            'name': user.name,

            'email': user.email,

            'reports': reports_count,

            'comp_count': compensations.count(),

            'total_comp': total_comp

        })

    return render(request, 'admin_dashboard.html', {
            'emergency_reports': emergency_reports,
            'normal_reports': normal_reports,
            'users_data': users_data,
            'notification': notification
        })


import base64
from django.shortcuts import render, redirect
from .models import Report
from .ai import detect_issue

def submit_report(request):
    if request.method == 'POST':

        desc = request.POST.get('description', 'SOS Emergency')
        loc = request.POST.get('location')
        image_data = request.POST.get('image')

        # 🔥 convert base64 → image file
        if image_data:
            format, imgstr = image_data.split(';base64,')
            file_data = base64.b64decode(imgstr)

            path = f"media/sos_{int(time.time())}.jpg"
            with open(path, 'wb') as f:
                f.write(file_data)
        else:
            path = None

        # AI detection
        ai_result = detect_emergency(path) if path else "No Image"
        if ai_result == "Invalid Emergency":
            return render(request, 'emergency.html', {
        'error': 'Please upload a valid accident image'
    })
        if ai_result != "Invalid Emergency":
            Notification(
                message=f"New emergency report: {desc} at {loc}"
            ).save()
        infra_result = detect_issue(path) 
        if infra_result == "Pothole":
            final_result = "Possible pothole-related accident"
        elif infra_result == "Road Blockage":
            final_result = "Possible road blockage accident"
        else:
            final_result = "General accident"

        Report(
            description=desc,
            location=loc,
            image=path if path else "No Image",
            ai_result=final_result,
            user_email="Emergency User",
            status="Pending"
        ).save()

        return redirect('/emergency/')

    return render(request, 'emergency.html')


def dashboard(request):
    return render(request, 'dashboard.html')  

def emergency(request):
    return render(request, 'emergency.html') 

from .ai import detect_issue
import base64, time

def submit_dashboard_report(request):
    if request.method == 'POST':

        desc = request.POST.get('description')
        loc = request.POST.get('location')
        image_data = request.POST.get('image')

        path = None

        # 🔥 SAVE IMAGE (IMPORTANT for AI)
        if image_data:
            format, imgstr = image_data.split(';base64,')
            file_data = base64.b64decode(imgstr)

            path = f"media/report_{int(time.time())}.png"
            with open(path, 'wb') as f:
                f.write(file_data)

        # 🔥 AI DETECTION
        ai_result = detect_issue(path) if path else "No Image"

        if desc == "SOS Emergency":
            type = "Emergency"
        else:
            type = "Normal"

        # 🔥 SAVE TO DB
        Report(
            user_email=request.session.get('user'),
            description=desc,
            location=loc,
            image=path,
            ai_result=ai_result
        ).save()

        return redirect('/dashboard/')
    
def delete_report(request, report_id):
        Report.objects(id=report_id).delete()
        
        return redirect('/admin_dashboard/')

def dashboard(request):

    user_email = request.session.get('user')

    # USER REPORTS
    reports = Report.objects(
        user_email=user_email
    ).order_by('-created_at')

    # USER COMPENSATIONS
    compensations = Compensation.objects(
        victim_email=user_email
    ).order_by('-created_at')

    return render(
        request,
        'dashboard.html',
        {
            'reports': reports,
            'compensations': compensations
        }
    )


def approve_compensation(request, report_id):

    report = Report.objects(id=report_id).first()

    if not report:
        return redirect('/admin_dashboard/')

    victim_email = request.GET.get('email')

    amount = request.GET.get('amount')

    Compensation(

        victim_email=victim_email,

        report_id=str(report.id),

        ai_result=report.ai_result,

        amount=float(amount),

        status="Approved"

    ).save()

    report.status = "Compensation Approved"

    report.save()

    return redirect('/admin_dashboard/')