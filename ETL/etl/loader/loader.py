from datetime import datetime
from os import environ

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from loguru import logger

from storage.storage import State

from .utilities import es_backoff

load_dotenv()

CHUNK_SIZE = int(environ.get('ETL_CHUNK_SIZE'))

es = Elasticsearch(
    hosts=[f"{environ.get('ELASTIC_HOST')}:{environ.get('ELASTIC_PORT')}"]
)


@es_backoff(start_sleep_time=0.5, factor=2, border_sleep_time=10)
def create_index(index_name: str, index_body: str):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_body)
        logger.info(f'Create index: {index_name}')


@es_backoff(start_sleep_time=0.5, factor=2, border_sleep_time=10)
def es_index_is_empty(index: str) -> bool:
    response = es.search(index=index)
    loaded_items = response['hits']['total']['value']
    return True if loaded_items == 0 else False


class ESLoader:
    def __init__(self, data: list[dict], state: State, index: str):
        self.data = data
        self.state = state
        self.index = index

    def es_bulk_data_generator(self):
        for chunk in self.data:
            for item in chunk:
                es_index = {"_index": self.index, "_id": item["id"]}
                es_index.update(item)
                yield es_index

    def load_data_to_es(self):
        if self.data:
            for ok, info in streaming_bulk(es, self.es_bulk_data_generator(), chunk_size=CHUNK_SIZE):
                if not ok:
                    logger.error('An error occurred while loading: ', info)
                else:
                    last_extracted = datetime.now()
                    self.state.set_state('last_checked', last_extracted.strftime('%Y-%m-%d %H:%M:%S'))
