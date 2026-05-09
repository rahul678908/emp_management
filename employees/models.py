from django.db import models
import json


class DynamicForm(models.Model):
    name = models.CharField(max_length=200)
    fields = models.JSONField(default=list)  # List of {label, type, order, required}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_fields(self):
        return sorted(self.fields, key=lambda f: f.get('order', 0))


class Employee(models.Model):
    form = models.ForeignKey(DynamicForm, on_delete=models.SET_NULL, null=True, related_name='employees')
    data = models.JSONField(default=dict)  # {field_label: value}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Try to find a name-like field
        for key in ('name', 'Name', 'full_name', 'Full Name', 'employee_name'):
            if key in self.data:
                return self.data[key]
        return f"Employee #{self.pk}"

    def get_display_data(self):
        if self.form:
            result = []
            for field in self.form.get_fields():
                label = field.get('label', '')
                result.append({
                    'label': label,
                    'type': field.get('type', 'text'),
                    'value': self.data.get(label, ''),
                })
            return result
        return [{'label': k, 'type': 'text', 'value': v} for k, v in self.data.items()]
