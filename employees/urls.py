from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # Employee CRUD
    path('', views.employee_list, name='list'),
    path('create/', views.employee_create, name='create'),
    path('<int:pk>/edit/', views.employee_edit, name='edit'),
    path('save/', views.employee_save, name='save'),
    path('<int:pk>/delete/', views.employee_delete, name='delete'),

    # Form builder
    path('forms/', views.form_list, name='form_list'),
    path('forms/create/', views.form_create, name='form_create'),
    path('forms/<int:pk>/edit/', views.form_edit, name='form_edit'),
    path('forms/save/', views.form_save, name='form_save'),
    path('forms/<int:pk>/delete/', views.form_delete, name='form_delete'),
    path('forms/<int:pk>/fields/', views.get_form_fields, name='form_fields'),
]
