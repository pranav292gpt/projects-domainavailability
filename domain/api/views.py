from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pythonwhois
from django.http.response import HttpResponse
import requests

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

from rest_framework.parsers import JSONParser

class Test(APIView):

    PAGE_ACCESS_TOKEN  = 'EAACIFCtpPWMBAOg0rbEVPf5v2uAlDlh5Y22Ks336ZBSm96zz7t3mv8y7qacCEwJC9JUJyfxsCNifWWeMgTvB0wkboFAKMHGUjVBTIRbBWPpscGW50z6UNFASNcSFaAOpfaOnQ1G2HsMGgOQmdpX8mkqTR9g8gqWRAQceOOAZDZD'
    standard_greetings = ['hello', 'hi', 'hey', 'morning', 'good morning', 'hii', 'greetings']

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('hub.verify_token'):
            print self.request.GET['hub.verify_token']
            print self.request.GET['hub.challenge']
            return HttpResponse(self.request.GET['hub.challenge'])
        return Response({"Hello": "World"})
	
    def post(self, request, *ags, **kwargs):
		
	    webhook_event =  request.data['entry'][0]['messaging'][0]
	    sender_psid = webhook_event['sender']['id']
	    message = webhook_event.get('message')

	    print sender_psid

	    if message:
		message['text'].lower()
		if message['text'].lower() in self.standard_greetings:
		    response = {'text': "{0} \nPlease enter a domain name to check availability.".format(message['text'].title())}
    	    	else: 		
		    domain = message['text']
		    print domain
		    
		    try: 
			query = pythonwhois.get_whois(domain)
		    	if not query.get("id"):
			    response = {"text": "Congratulations. The requested domain {0} is available.".format(domain)}
			else:
			    creation_date=str(query.get("creation_date")[0])
			    expiration_date = str(query.get("expiration_date")[0])
			    response = {"text" : "Sorry. The requested domain {0} is not available.\n".format(domain) +
			"The requested domain was created on {0} and expires on {1}.".format(creation_date, expiration_date)}
		    except Exception as exception:
			print exception
			response = {'text':"Please enter a valid domain name."}



	    	req = requests.post("https://graph.facebook.com/v2.6/me/messages", 
		json={
		    "access_token": self.PAGE_ACCESS_TOKEN,
		    "recipient": {"id": sender_psid},
		    "message": response
		  })
		print req.text

		return Response({'received data': request.data})
