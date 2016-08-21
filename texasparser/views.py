from django.shortcuts import render
from django.http.response import JsonResponse

# Create your views here.


from texasparser.models import Files



def get_values(request):

    try:
        file_objs = Files.objects.all()

        result = {}

        result["result"] = "Success"
        result["data"] = []

        for file_obj in file_objs:
            result["data"].append(file_obj.data)

        return JsonResponse(result)
    except Exception as err:
        return JsonResponse({"Error": "Unable to serve your request " + err})




