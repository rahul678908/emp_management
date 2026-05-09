from django.urls import path
from .api_views import (
    DynamicFormListCreateAPIView, DynamicFormDetailAPIView,
    EmployeeListCreateAPIView, EmployeeDetailAPIView
)

urlpatterns = [
    path('forms/', DynamicFormListCreateAPIView.as_view(), name='api_form_list'),
    path('forms/<int:pk>/', DynamicFormDetailAPIView.as_view(), name='api_form_detail'),
    path('employees/', EmployeeListCreateAPIView.as_view(), name='api_employee_list'),
    path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='api_employee_detail'),
]
