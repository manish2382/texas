from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json

# Create your views here.


from texasparser.models import Files
import os


def get_value(request, obj_id):

    result = {}
    result["status"] = "Failure"
    try:
        file_obj = Files.objects.get(id=obj_id)
        result["status"] = "Success"
        result["data"] = file_obj.data
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result["data"] = "Does not exists"
        return JsonResponse(result)
    except:
        result["data"] = "Unable to serve request"
        return JsonResponse(result)


def get_values(request):

    try:
        file_objs = Files.objects.all()

        result = {}

        result["status"] = "Success"
        result["data"] = []

        for file_obj in file_objs:
            result["data"].append(file_obj.data)

        return JsonResponse(result)
    except:
        return JsonResponse({"Error": "Unable to serve request."})




