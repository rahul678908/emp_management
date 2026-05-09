import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import DynamicForm, Employee


# ---- Form Builder Views ----

@login_required
def form_list(request):
    forms = DynamicForm.objects.all().order_by('-created_at')
    return render(request, 'employees/form_list.html', {'forms': forms})


@login_required
def form_create(request):
    return render(request, 'employees/form_builder.html', {'form_obj': None})


@login_required
def form_edit(request, pk):
    form_obj = get_object_or_404(DynamicForm, pk=pk)
    return render(request, 'employees/form_builder.html', {'form_obj': form_obj})


@login_required
@require_http_methods(['POST'])
def form_save(request):
    try:
        body = json.loads(request.body)
        name = body.get('name', '').strip()
        fields = body.get('fields', [])
        form_id = body.get('id')
        if not name:
            return JsonResponse({'error': 'Form name is required.'}, status=400)
        if form_id:
            form_obj = get_object_or_404(DynamicForm, pk=form_id)
            form_obj.name = name
            form_obj.fields = fields
            form_obj.save()
        else:
            form_obj = DynamicForm.objects.create(name=name, fields=fields)
        return JsonResponse({'id': form_obj.pk, 'name': form_obj.name, 'message': 'Form saved successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def form_delete(request, pk):
    if request.method == 'DELETE' or request.method == 'POST':
        form_obj = get_object_or_404(DynamicForm, pk=pk)
        form_obj.delete()
        return JsonResponse({'message': 'Form deleted.'})
    return JsonResponse({'error': 'Method not allowed.'}, status=405)


# ---- Employee Views ----

@login_required
def employee_list(request):
    employees = Employee.objects.select_related('form').all().order_by('-created_at')
    forms = DynamicForm.objects.all()
    search = request.GET.get('search', '').strip()
    field_filter = request.GET.get('field', '').strip()
    if search:
        filtered = []
        for emp in employees:
            for key, val in emp.data.items():
                if (not field_filter or key == field_filter) and search.lower() in str(val).lower():
                    filtered.append(emp)
                    break
        employees = filtered
    # Collect all unique field labels for filter dropdown
    all_fields = set()
    for emp in Employee.objects.select_related('form').all():
        if emp.form:
            for f in emp.form.fields:
                all_fields.add(f.get('label', ''))
    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'forms': forms,
        'all_fields': sorted(all_fields),
        'search': search,
        'field_filter': field_filter,
    })


@login_required
def employee_create(request):
    forms = DynamicForm.objects.all()
    return render(request, 'employees/employee_form.html', {'forms': forms, 'employee': None})


@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    forms = DynamicForm.objects.all()
    return render(request, 'employees/employee_form.html', {'forms': forms, 'employee': employee})


@login_required
@require_http_methods(['POST'])
def employee_save(request):
    try:
        body = json.loads(request.body)
        form_id = body.get('form_id')
        data = body.get('data', {})
        emp_id = body.get('id')
        form_obj = get_object_or_404(DynamicForm, pk=form_id)
        if emp_id:
            emp = get_object_or_404(Employee, pk=emp_id)
            emp.form = form_obj
            emp.data = data
            emp.save()
        else:
            emp = Employee.objects.create(form=form_obj, data=data)
        return JsonResponse({'id': emp.pk, 'message': 'Employee saved successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def employee_delete(request, pk):
    if request.method in ('DELETE', 'POST'):
        emp = get_object_or_404(Employee, pk=pk)
        emp.delete()
        return JsonResponse({'message': 'Employee deleted.'})
    return JsonResponse({'error': 'Method not allowed.'}, status=405)


@login_required
def get_form_fields(request, pk):
    form_obj = get_object_or_404(DynamicForm, pk=pk)
    return JsonResponse({'fields': form_obj.get_fields(), 'name': form_obj.name})
