########## ELASTICSEARCH CONFIGURATION
from elasticsearch import Elasticsearch, RequestsHttpConnection
from urlparse import urlparse
import os

ES_URL = os.environ.get('SEARCHBOX_URL') or 'http://127.0.0.1:9200/'

if not urlparse(ES_URL).port:
    ES_URL += ':80'
ES_CLIENT = Elasticsearch([ES_URL], connection_class=RequestsHttpConnection)
########## END ELASTICSEARCH CONFIGURATION

