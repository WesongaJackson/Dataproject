
from django.urls import path


from main_app import views

urlpatterns = [
    path('', views.home, name="home"),
    path('employees/', views.all_employees, name="all"),
    path('employees/<int:emp_id>/', views.employee_details, name="details"),
    path('employees/delete/<int:emp_id>/', views.employee_delete, name="delete"),
    path('employees/update/<int:emp_id>/', views.update_employee, name="update"),
    path('search/', views.search_employees, name="search"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),

]
# "employees/<int:emp_id>"
# tables
# user

# admin , admin@gmail.com , 123456

# python manage.py migrate
# python manage.py createsuperuser
