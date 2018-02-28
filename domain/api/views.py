from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pythonwhois
from django.http.response import HttpResponse

class DomainChecker(APIView):
    def get(self, request, *args, **kwargs):
        if "domain" in request.GET:
            domain = request.GET.get("domain")

            try:
                query = pythonwhois.get_whois(domain)
            

                if not query.get("id"):
                    response = {
                            "domain" : domain,
                            "available" : True
                            }
                    return Response(response)
                
                response = {
                        "domain" : domain,
                        "creation_date" : str(query.get("creation_date")[0]),
                        "expiration_date" : str(query.get("expiration_date")[0]),
                        "updated_date" : str(query.get("updated_date")[0]),
                        "available" : False
                        }
                return Response(response)
            except Exception:
                return Response({"error" : " No root WHOIS server found for domain."}, status.HTTP_400_BAD_REQUEST)
        return Response({"error" : "bad request"}, status.HTTP_400_BAD_REQUEST)

class Test(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('hub.verify_token'):
            print self.request.GET['hub.verify_token']
            print self.request.GET['hub.challenge']
            return HttpResponse(self.request.GET['hub.challenge'])
        return Response({"Hello": "World"})
