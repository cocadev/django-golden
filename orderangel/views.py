from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from elasticsearch import Elasticsearch
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

# ================
# Inner app module
# ================
from orderangel import settings

es = Elasticsearch(["54.37.77.15"],
                   http_auth=('oaboss', '066241908'),
                   port=9201,
                   )


def home(request):
    return render(request, "public/home.html")


########################################################################################################################
#                                                                                                                      #
#                                    Main Apis                                                                         #
#                                                                                                                      #
########################################################################################################################



@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def stores(request):
    if request.GET.get("store"):

        try:
            res = es.search(index="stores", doc_type='store', filter_path=['hits.hits._id', 'hits.hits._source'], body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "terms": {
                                    "store_id": request.GET.getlist("store")
                                }
                            }
                        ]
                    }
                }
            })
            return Response({
                "data": res["hits"]["hits"]
            })
        except:
            return Response(status=404)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def orders(request, user):
    return Response({'result': [

        {
            "key": "1",
            "company": "HERMANN ALBERS OBST & GEMÜSE GMBH",
            "date": "28.02.2018",
            "state": "In-Progress"

        },
        {
            "key": "2",
            "company": 'HERMANN ALBERS OBST & GEMÜSE GMBH',
            "date": "27.02.2018",
            "state": "Dispatched"

        }
    ]})


@api_view(['GET'])
def order(request, user, id):
    return JsonResponse({'result': [

        {
            "key": "1",
            "company": "HERMANN ALBERS OBST & GEMÜSE GMBH",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Banana_Fruit.JPG",
            "name": 'Banana',
            "unit": 'Gram',
            "price": 'EUR 1,20',
            "qty": "4",
            "date": "28.02.2018",
            "state": "In-Progress"

        },
        {
            "key": "2",
            "company": 'HERMANN ALBERS OBST & GEMÜSE GMBH',
            "logo": 'https://upload.wikimedia.org/wikipedia/commons/d/d3/Kiwi_aka.jpg',
            "name": 'Kiwi',
            "unit": 'Kilogram',
            "price": 'EUR 10,29',
            "qty": "2",
            "date": "27.02.2018",
            "state": "Dispatched"

        }
    ]}, safe=False, content_type='application/json')


########################################################################################################################
#                                                                                                                      #
#                                    Home Views                                                                        #
#                                                                                                                      #
########################################################################################################################


@login_required(login_url=settings.PUBLIC_LOGIN_URL)
def secure_profile(request):
    return render(request, 'public/profile.html',
                  {'user': request.user})


@login_required(login_url=settings.PUBLIC_LOGIN_URL)
def secure_account(request):
    return render(request, 'public/account.html',
                  {'user': request.user})
