'''
We store abstractions to control infrastructure here.
'''
from elasticsearch import Elasticsearch
client = Elasticsearch()


def create_index(index_name='django'):
    '''
    A command to make an index.
    Does not raise an exception in case index already exists.
    '''
    client.indices.create(
        index=index_name,
        ignore=400,
        timeout=60,
        master_timeout=15
    )


def delete(index_name):
    client.indices.delete(index=index_name)
