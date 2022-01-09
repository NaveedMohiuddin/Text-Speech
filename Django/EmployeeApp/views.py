from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from EmployeeApp.models import Departments,Employees
from EmployeeApp.serializers import DepartmentSerializer,EmployeeSerializer
from django.core.files.storage import default_storage
#import for sp-text
import speech_recognition as sr
from os import path
from pydub import AudioSegment

API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# Create your views here.
@csrf_exempt
def departmentApi(request,id=0):
    if request.method=='GET':
        departments = Departments.objects.all()
        departments_serializer = DepartmentSerializer(departments, many=True)
        return JsonResponse(departments_serializer.data, safe=False)

    elif request.method=='POST':
        department_data=JSONParser().parse(request)
        u_input=department_data['summ']

        minL=500
        maxL=1000
        output1 = query({
            "inputs":u_input,
            "parameters":{"min_length":minL,"max_length":maxL},
        })
        print("test")
        department_data['output']=output1[0]['summary_text']
        print(department_data['output'])
        print(department_data)

        department_serializer = DepartmentSerializer(data=department_data)
        # print(type(u_input))
        #NLP model

        # x={'output':output1}

        print(output1)
        print(department_serializer)

        if department_serializer.is_valid():
            # department_serializer.data['output']=output1
            # print(department_serializer)
            department_serializer.save()
            return JsonResponse("Add Successfully!!", safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        department_data = JSONParser().parse(request)
        department=Departments.objects.get(DepartmentId=department_data['DepartmentId'])
        department_serializer=DepartmentSerializer(department,data=department_data)
        if department_serializer.is_valid():
            department_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        department=Departments.objects.get(DepartmentId=id)
        department.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)

@csrf_exempt
def employeeApi(request,id=0):
    if request.method=='GET':
        employees = Employees.objects.all()
        employees_serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(employees_serializer.data, safe=False)

    elif request.method=='POST':
        employee_data=JSONParser().parse(request)

        filename=employee_data['PhotoFileName']

        dst = 'test.wav'   

        file='D:/Web dev/Django/DjangoReactJs-main/DjangoReactJs-main/Django/DjangoAPI/media/'+ filename
        print(file)
        print("Hellllloooooooooooo")
        
        if(file[len(file)-3:len(file)]!="wav"):
        
            AudioSegment.from_file(file).export(dst, format="wav")
            filename = dst
        else:
            filename = file
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            print(text) 
        employee_data['AudioText'] = text

        audiosumm = query({
            "inputs":text,
        })
        employee_data['AudioSummary']=audiosumm[0]['summary_text']
        employee_serializer = EmployeeSerializer(data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        employee_data = JSONParser().parse(request)
        employee=Employees.objects.get(EmployeeId=employee_data['EmployeeId'])
        employee_serializer=EmployeeSerializer(employee,data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        employee=Employees.objects.get(EmployeeId=id)
        employee.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)


@csrf_exempt
def SaveFile(request):
    file=request.FILES['myFile']
    file_name = default_storage.save(file.name,file)

    return JsonResponse(file_name,safe=False)