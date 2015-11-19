'''
We store abstractions to control infrastructure here.
'''
from elasticsearch import Elasticsearch


def create_index(index_name='django'):
    '''
    A command to make an index
    '''
    client = Elasticsearch()
    client.indices.create(index=index_name, ignore=400)
