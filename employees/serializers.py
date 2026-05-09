from rest_framework import serializers
from .models import DynamicForm, Employee


class DynamicFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicForm
        fields = ['id', 'name', 'fields', 'created_at', 'updated_at']


class EmployeeSerializer(serializers.ModelSerializer):
    form_name = serializers.CharField(source='form.name', read_only=True)
    display_data = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'form', 'form_name', 'data', 'display_data', 'created_at', 'updated_at']

    def get_display_data(self, obj):
        return obj.get_display_data()
