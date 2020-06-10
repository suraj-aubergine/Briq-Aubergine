from django.shortcuts import render
from briq_sentiment_quote import settings
from rest_framework.response import Response
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import requests
from rest_framework.views import APIView
import random

# Create your views here.

def detect_sentiment(text):
    comprehend = boto3.client(service_name='comprehend', region_name='ap-southeast-1', aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY,)

    sentiment = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)

    return sentiment
    

def get_all_quotes():
    url = 'https://programming-quotes-api.herokuapp.com/quotes'

    data = requests.get(url)

    return data

def create_doc(quote, sentiment):
    quote.pop('_id')
    quote["SentimentScore"] = json.loads(sentiment)["SentimentScore"]

    host = 'search-briq-aubergine-demo-5yssyyidfsj4wquhpgrvqt7chm.eu-west-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
    region = 'eu-west-1' # e.g. us-west-1

    service = 'es'
    awsauth = AWS4Auth(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY, region, service, session_token=credentials.token)

    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    document = quote

    es.index(index="quotes", doc_type="_doc", id=quote['id'], body=document)


def loop_through_all_quotes():
    data = get_all_quotes()
    
    for quote in json.loads(data.text):
        quote_text = quote['en']
        sentiment = detect_sentiment(quote_text)
        create_doc(quote, sentiment)

class Suggest_Quote(APIView):
    def post(self, request):
        quote_id = request.data['quoteId']
        new_rate = request.data['newVote']
        host = 'search-briq-aubergine-demo-5yssyyidfsj4wquhpgrvqt7chm.eu-west-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
        region = 'eu-west-1' # e.g. us-west-1

        service = 'es'
        awsauth = AWS4Auth(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY, region, service)

        es = Elasticsearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )

        doc = es.get(index="quotes", doc_type="_doc", id=quote_id)
        
        if new_rate > 3:
            body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"gt": doc["_source"]["SentimentScore"]["Positive"]}}}]}}, "sort":{"SentimentScore.Positive": {"order":"asc"}}}
            result = es.search(index="quotes", body=body)
            length = len(result["hits"]["hits"])
            if length == 0:
                body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"lt": doc["_source"]["SentimentScore"]["Positive"]}}}]}}, "sort":{"SentimentScore.Positive": {"order":"desc"}}}
                result = es.search(index="quotes", body=body)
                length=len(result["hits"]["hits"])
            n = random.randint(0,length-1)
            return Response(result["hits"]["hits"][n])
        else:
            if doc['_source']['SentimentScore']['Positive'] < 0.5:
                body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"gt": doc["_source"]["SentimentScore"]["Positive"]}}}]}}, "sort":{"SentimentScore.Positive": {"order":"desc"}}}
                result = es.search(index="quotes", body=body)
                length = len(result["hits"]["hits"])
                if length == 0:
                    body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"gt": doc["_source"]["SentimentScore"]["Positive"]}}}]}}, "sort":{"SentimentScore.Positive": {"order":"desc"}}}
                    result = es.search(index="quotes", body=body)
                    length=len(result["hits"]["hits"])
                n = random.randint(0,length-1)
                print(length)
                print(n)
                return Response(result["hits"]["hits"][n])

            else:
                body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"lt": doc["_source"]["SentimentScore"]["Positive"]}}}]}}, "sort":{"SentimentScore.Positive": {"order":"asc"}}}
                result = es.search(index="quotes", body=body)
                length = len(result["hits"]["hits"])
                if length == 0:
                    body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"gt": doc["_source"]["SentimentScore"]["Positive"]}}}]}}, "sort":{"SentimentScore.Positive": {"order":"asc"}}}
                    result = es.search(index="quotes", body=body)
                    length=len(result["hits"]["hits"])
                n = random.randint(0,length-1)
                print(length)
                print(n)
                return Response(result["hits"]["hits"][n])

class Get_New_Quote(APIView):

    def post(self, request):
        positive_sentiment = request.data['positiveSentiment']
        host = 'search-briq-aubergine-demo-5yssyyidfsj4wquhpgrvqt7chm.eu-west-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
        region = 'eu-west-1' # e.g. us-west-1

        service = 'es'
        awsauth = AWS4Auth(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY, region, service)

        es = Elasticsearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )


        if positive_sentiment < 0.5:
            body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"lt": positive_sentiment}}}]}}, "sort":{"SentimentScore.Positive": {"order":"asc"}}}
            result = es.search(index="quotes", body=body)
            length = len(result["hits"]["hits"])
            if length == 0:
                body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"gt": positive_sentiment}}}]}}, "sort":{"SentimentScore.Positive": {"order":"asc"}}}
                result = es.search(index="quotes", body=body)
                length=len(result["hits"]["hits"])
            n = random.randint(0,length-1)
            return Response(result["hits"]["hits"][n])

        else:
            body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"gt": positive_sentiment}}}]}}, "sort":{"SentimentScore.Positive": {"order":"desc"}}}
            result = es.search(index="quotes", body=body)
            length = len(result["hits"]["hits"])
            if length == 0:
                body = {"query":{"bool":{"must":[{"match_all":{}}],"filter":[{"range":{"SentimentScore.Positive":{"lt": positive_sentiment}}}]}}, "sort":{"SentimentScore.Positive": {"order":"desc"}}}
                result = es.search(index="quotes", body=body)
                length=len(result["hits"]["hits"])
            n = random.randint(0,length-1)
            return Response(result["hits"]["hits"][n])

class Get_quote(APIView):
    def get(self, request, quoteId):
        quote_id = quoteId
        print(quote_id)
        host = 'search-briq-aubergine-demo-5yssyyidfsj4wquhpgrvqt7chm.eu-west-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
        region = 'eu-west-1' # e.g. us-west-1

        service = 'es'
        awsauth = AWS4Auth(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY, region, service)

        es = Elasticsearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )
        body = {"query": {"term": {"id": {"value": quote_id}}}}
        result = es.search(index="quotes", body=body)
        return Response(result["hits"]["hits"][0])
