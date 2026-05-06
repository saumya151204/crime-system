from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CrimeReportForm
from .models import CrimeReport


#  LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


#  LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


#  HOME
def home(request):
    return render(request, 'home.html')


#  DASHBOARD
@login_required
def dashboard(request):
    reports = CrimeReport.objects.filter(user=request.user)

    # counts yahi calculate honge (not outside)
    pending_count = reports.filter(status='Pending').count()
    progress_count = reports.filter(status='In Progress').count()
    resolved_count = reports.filter(status='Resolved').count()

    return render(request, 'dashboard.html', {
        'reports': reports,
        'pending_count': pending_count,
        'progress_count': progress_count,
        'resolved_count': resolved_count
    })


#  CREATE REPORT
@login_required
def create_report(request):
    if request.method == "POST":
        form = CrimeReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user

            #  force default status
            report.status = 'Pending'

            report.save()
            return redirect('dashboard')
    else:
        form = CrimeReportForm()

    return render(request, 'create_report.html', {'form': form})


#  REPORT DETAIL
@login_required
def report_detail(request, id):
    report = get_object_or_404(CrimeReport, id=id)
    return render(request, 'report_detail.html', {'report': report})


#  STATUS TOGGLE (FEATURE)
@login_required
def update_status(request, id):
    report = get_object_or_404(CrimeReport, id=id)

    if report.user != request.user:
        return redirect('dashboard')

    #  3-step cycle
    if report.status == 'Pending':
        report.status = 'In Progress'

    elif report.status == 'In Progress':
        report.status = 'Resolved'

    else:
        report.status = 'Pending'

    report.save()
    return redirect('dashboard')