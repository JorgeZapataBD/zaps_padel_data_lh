import json
import logging
from datetime import date, datetime
from typing import Literal

import pyarrow as pa
import pyarrow.parquet as pq
from airflow.models import Variable
from requests.auth import AuthBase
from zaps_core.clients.firestore_client import FirestoreClient
from zaps_core.clients.gcs_client import GCSClient
from zaps_core.clients.http_client import HttpClient

from plugins.zaps_padel.utils.utils_pyarrow import get_pyarrow_schema

logger = logging.getLogger(__name__)


class FantasyPadelAuth(AuthBase):
    def __init__(self):
        self.api_token = Variable.get('ZAPS_PADEL_FANTASY_TOKEN_API_KEY')

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.api_token}'
        return r


def get_headers():
    """
    Create the specific headers to connect with padel fantasy API
    output:
        headers: specific headers to connect with padel intelligence Api,
                        including authorization token (dict)
    """
    headers = dict()
    headers["Accept"] = ("application/json")
    return headers


def operator_padel_fantasy_list2gcs(
    api_endpoint: Literal['players', 'seasons', 'seasons_tournaments', 'matches'],
    api_params: dict,
    gcp_project_id: str,
    gcp_conn_id: str,
    gcs_bucket: str,
):
    """
    Function that makes requests to the API of padel fantasy with the created client and then ingests
    the data in BigQuery, also manages the offset of the API,
    in this case through a datetime with Google Firestore.
    Args:
        :param gcp_project_id: GCP Project (str)
        :param gcp_conn_id: GCP Airflow Connection (str)
        :param bq_dataset_id: Destination BigQuery Dataset (str)
        :param bq_table_id: Destination BigQuery Table (str)
        :param bq_schema_fields: BigQuery schema fields (list)
    """
    # Create unique bucket by environment
    gcs_bucket = f'{gcp_project_id.split("-")[0]}_{gcs_bucket}'
    d_params = {'per_page': api_params['per_page'], 'page': api_params['page']}
    # Get data from padel fantasy
    response = HttpClient(Variable.get('ZAPS_PADEL_FANTASY_BASE_URL')).get_data(
        endpoint=f'api/{api_endpoint}',
        headers=get_headers(),
        auth=FantasyPadelAuth(),
        **d_params
    )
    # Check if there are new data
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as e:
        logger.error(f'Json Decoded Error: {e}')
        raise e
    if data['data']:
        # Filter data to get only new ids
        if api_endpoint != 'matches':
            filter_data = [resource for resource in data['data']
                           if resource['id'] not in api_params['ids']]
        else:
            filter_data = [
                resource
                for resource in data['data']
                if resource['id'] not in api_params['ids'] and datetime.strptime(resource['played_at'], '%Y-%m-%d').date() < date.today()
            ]
        ids_list = [resource['id']
                    for resource in filter_data] + api_params['ids']
        if filter_data:
            if api_endpoint != 'seasons':
                # Convert JSON to Arrow Table
                s_local_file = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{api_endpoint}_size_{api_params["per_page"]}_page_{api_params["page"]}.parquet'
                # Get pyarrow schema and create parquet file
                pa_schema = get_pyarrow_schema(
                    'padel_fantasy_schemas', api_endpoint)
                pa_table = pa.Table.from_pylist(filter_data, schema=pa_schema)
                pq.write_table(pa_table, f'/tmp/{s_local_file}')
                # Upload the file to the destination bucket
                client_gcs = GCSClient(gcp_project_id, gcp_conn_id)
                client_gcs.upload_file(
                    bucket_name=gcs_bucket,
                    source_file=f'/tmp/{s_local_file}',
                    destination_blob_name=f"{api_endpoint}/date={date.today().strftime('%Y-%m-%d')}/{s_local_file}"
                )
            # Create Firestore client and update document with news ids
            fs_client = FirestoreClient(gcp_project_id, gcp_conn_id)
            # Change page if all elements have been readed
            if len(filter_data) == api_params['per_page']:
                api_params['page'] = api_params['page'] + 1
            api_params['ids'] = api_params['ids'] + ids_list
            fs_client.add_or_update_document(
                collection_name='padel_fantasy',
                doc_id=api_endpoint,
                data=api_params
            )
            return True
        else:
            logger.info(
                f'There are not new data for {api_endpoint} from padel fantasy API')
            return False


def operator_padel_fantasy_fromobject2gcs(
    api_endpoint: Literal['seasons_tournaments', 'matches_stats'],
    api_params: dict,
    gcp_project_id: str,
    gcp_conn_id: str,
    gcs_bucket: str,
):
    """
    Function that makes requests to the API of padel fantasy with the created client and then ingests
    the data in BigQuery, also manages the offset of the API,
    in this case through a datetime with Google Firestore.
    Args:
        :param gcp_project_id: GCP Project (str)
        :param gcp_conn_id: GCP Airflow Connection (str)
        :param bq_dataset_id: Destination BigQuery Dataset (str)
        :param bq_table_id: Destination BigQuery Table (str)
        :param bq_schema_fields: BigQuery schema fields (list)
    """
    # Create unique bucket by environment
    gcs_bucket = f'{gcp_project_id.split("-")[0]}_{gcs_bucket}'
    d_params = {'per_page': api_params['per_page']}
    # Get data from padel fantasy
    response = HttpClient(Variable.get('ZAPS_PADEL_FANTASY_BASE_URL')).get_data(
        endpoint=f'api/{api_endpoint.split("_")[0]}/{api_params["page"]}/{api_endpoint.split("_")[1]}',
        headers=get_headers(),
        auth=FantasyPadelAuth(),
        **d_params
    )
    # Check if there are new data
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as e:
        logger.error(f'Json Decoded Error: {e}')
        raise e
    if data['data']:
        # Filter data to get only new ids
        filter_data = [resource for resource in data['data']
                       if resource['id'] not in api_params['ids']]
        ids_list = [resource['id']
                    for resource in filter_data] + api_params['ids']
        if filter_data:
            # Convert JSON to Arrow Table
            s_local_file = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{api_endpoint}_size_{api_params["per_page"]}_page_{api_params["page"]}.parquet'
            # Get pyarrow schema and create parquet file
            pa_schema = get_pyarrow_schema(
                'padel_fantasy_schemas', api_endpoint)
            pa_table = pa.Table.from_pylist(filter_data, schema=pa_schema)
            pq.write_table(pa_table, f'/tmp/{s_local_file}')
            # Upload the file to the destination bucket
            client_gcs = GCSClient(gcp_project_id, gcp_conn_id)
            client_gcs.upload_file(
                bucket_name=gcs_bucket,
                source_file=f'/tmp/{s_local_file}',
                destination_blob_name=f"{api_endpoint}/date={date.today().strftime('%Y-%m-%d')}/{s_local_file}"
            )
            # Create Firestore client and update document with news ids
            fs_client = FirestoreClient(gcp_project_id, gcp_conn_id)
            # Change page if all elements have been readed
            if len(filter_data) == api_params['per_page']:
                api_params['page'] = api_params['page'] + 1
            api_params['ids'] = api_params['ids'] + ids_list
            api_params[f'{api_endpoint.split("_")[0]}_ids'] = api_params[f'{api_endpoint.split("_")[0]}_ids'] + [
                api_params["page"]]
            fs_client.add_or_update_document(
                collection_name='padel_fantasy',
                doc_id=api_endpoint,
                data=api_params
            )
            return True
        else:
            logger.info(
                f'There are not new data for {api_endpoint} from padel fantasy API')
            return False
