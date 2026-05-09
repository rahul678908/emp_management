from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import DynamicForm, Employee
from .serializers import DynamicFormSerializer, EmployeeSerializer


class DynamicFormListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        forms = DynamicForm.objects.all().order_by('-created_at')
        return Response(DynamicFormSerializer(forms, many=True).data)

    def post(self, request):
        serializer = DynamicFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DynamicFormDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        form = get_object_or_404(DynamicForm, pk=pk)
        return Response(DynamicFormSerializer(form).data)

    def put(self, request, pk):
        form = get_object_or_404(DynamicForm, pk=pk)
        serializer = DynamicFormSerializer(form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        form = get_object_or_404(DynamicForm, pk=pk)
        form.delete()
        return Response({'message': 'Form deleted.'}, status=status.HTTP_204_NO_CONTENT)


class EmployeeListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Employee.objects.select_related('form').all().order_by('-created_at')
        search = request.query_params.get('search', '').strip()
        field = request.query_params.get('field', '').strip()
        if search:
            filtered = []
            for emp in queryset:
                for key, val in emp.data.items():
                    if (not field or key == field) and search.lower() in str(val).lower():
                        filtered.append(emp)
                        break
            queryset = filtered
        return Response(EmployeeSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        emp = get_object_or_404(Employee, pk=pk)
        return Response(EmployeeSerializer(emp).data)

    def put(self, request, pk):
        emp = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(emp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        emp = get_object_or_404(Employee, pk=pk)
        emp.delete()
        return Response({'message': 'Employee deleted.'}, status=status.HTTP_204_NO_CONTENT)
