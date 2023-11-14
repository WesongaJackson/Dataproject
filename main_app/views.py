from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django .contrib.auth.decorators import login_required,permission_required
from main_app.app_forms import EmployeeForm, LoginForm
from django.contrib import messages
from main_app.models import Employee
from django.contrib.auth import authenticate, login, logout


# Create your views here.
@login_required
@permission_required('main_app.add_employee',raise_exception=True)
def home(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "This employee updated successfully")
            return redirect("home")

    else:
        form = EmployeeForm()
    return render(request, "employee.html", {"form": form})


# Model View Template

# All employees
# One employee

@login_required
def all_employees(request):
    employees = Employee.objects.all()  # SELECT * FROM employees
    # employees = Employee.objects.all().order_by("-salary")
    # employees = Employee.objects.filter(name__istartswith="La").order_by("dob")
    # employees = Employee.objects.filter(name__istartswith="La", salary__gt=45000).order_by("dob")
    # employees = Employee.objects.filter(Q(name__contains="la") | Q(salary__gt=70000))
    # employees = Employee.objects.filter(Q(name__contains="la") & Q(salary__gt=70000))
    # employees = Employee.objects.filter(Q(name__contains="la") & ~Q(salary__gt=70000)) # tilde
    # today = datetime.today()
    # day = today.day
    # month = today.month
    # employees = Employee.objects.filter(dob__day=day, dob__month=month)  # tilde

    paginator = Paginator(employees, 20)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request, "all_employees.html", {"employees": data})

@login_required
@permission_required('main_app.view_employee',raise_exception=True)
def employee_details(request, emp_id):
    employee = Employee.objects.get(pk=emp_id)  # SELECT * FROM employees WHERE id=1
    return render(request, "employee_details.html", {"employee": employee})


# employees/delete/12000
@login_required
@permission_required('main_app.delete_employee',raise_exception=True)
def employee_delete(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)
    employee.delete()

    messages.error(request, "This employee was deleted permanently ")
    return redirect("all")

@login_required
@permission_required('main_app.view_employee',raise_exception=True)
def search_employees(request):
    search_word = request.GET["search_word"]
    employees = Employee.objects.filter(Q(name__icontains=search_word) | Q(email__icontains=search_word))
    paginator = Paginator(employees, 20)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request, "all_employees.html", {"employees": data})

@login_required
@permission_required('main_app.change_employee',raise_exception=True)
def update_employee(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "This employee updated successfully")
            return redirect('details', emp_id)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, "update.html", {'form': form})


def signin(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.error(request, "Invalid credentials")
        return render(request, 'login.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('signin')
