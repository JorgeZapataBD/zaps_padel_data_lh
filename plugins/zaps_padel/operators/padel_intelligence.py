import json
import logging
from datetime import date, datetime
from typing import Literal

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from airflow.models import Variable
from requests.auth import AuthBase
from zaps_core.clients.firestore_client import FirestoreClient
from zaps_core.clients.gcs_client import GCSClient
from zaps_core.clients.http_client import HttpClient

logger = logging.getLogger(__name__)


class PadelIntelligenceAuth(AuthBase):
    def __init__(self):
        self.api_token = Variable.get('ZAPS_PADEL_INTELLIGENCE_TOKEN_API_KEY')

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.api_token}'
        return r


def manage_stats_requests(
    id: int,
    stats_type: Literal['sets', 'player', 'team', 'lastpoints'] = None
) -> list:
    """
    Function that get stats of diferents parameters dependiend endpoint request
    from Padel Intelligence.

    :param id: match id to get stats
    :param stats_type: Stats type to get info of any match
    :return l_stats_info: python list to load to GCS
    """
    if stats_type == 'sets':
        l_stats_info = []
        for set_id in ['1', '2', '3']:
            r_response = HttpClient(f"{Variable.get('ZAPS_PADEL_INTELLIGENCE_BASE_URL')}/match/stats/{str(id)}/{set_id}").get_data(
                auth=PadelIntelligenceAuth(),
            )
            try:
                data = json.loads(r_response.text)
                l_stats_info.append(data)
            except json.JSONDecodeError as e:
                logger.error(f'Json Decoded Error: {e}')
                raise e
    else:
        if stats_type:
            url = f'https://realtime.padelintelligence.live/live/stats/{str(id)}/{stats_type}'
        else:
            url = f'https://realtime.padelintelligence.live/live/score/{str(id)}'
        with HttpClient(url).get_data(
            stream=True
        ) as r_response:
            # Open stream sesion get first line, parsed data and close
            for line in r_response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data:"):
                        json_data = decoded_line[5:].strip()
                        try:
                            l_stats_info = [json.loads(json_data)]
                        except json.JSONDecodeError as e:
                            logger.error(f'Json Decoded Error: {e}')
                            raise e
                    break
            else:
                l_stats_info = []
    return l_stats_info


def operator_pi_get_match_list2gcs(
    gcp_project_id: str,
    gcp_conn_id: str,
    gcs_bucket: str
):
    """
    Function that makes requests to the API of padel intelligence with the created client and then ingests
    the data in GCS, also manages the offset of the API,
    in this case through a page and id with Google Firestore.

    :param gcp_project_id: GCP project ID
    :param gcp_conn_id: Airflow connection ID to connect to GCP
    :param gcs_bucket: Target GCS bucket
    :return: Bool that define if any match has been ingested
    """
    # Bool to define if there is new data
    b_is_new_data = False
    # Create unique bucket by environment
    gcs_bucket = f'{gcp_project_id.split("-")[0]}_{gcs_bucket}'
    while True:
        # Check if we have offset for specific endpoint
        fs_client = FirestoreClient(gcp_project_id, gcp_conn_id)

        d_matches = fs_client.get_document(
            collection_name='padel_intelligence',
            doc_id='matches_list'
        )
        # Creating params request
        d_params = {'page': 0, 'size': 50, 'sort': 'Id'}
        if d_matches:
            d_params['page'] = d_matches['page']
        else:
            d_matches = {'page': 0, 'ids': [], 'size': d_params['size']}
        # Get data from padel intelligence api
        r_response = HttpClient(Variable.get('ZAPS_PADEL_INTELLIGENCE_BASE_URL')).get_data(
            endpoint='matches',
            auth=PadelIntelligenceAuth(),
            **d_params
        )
        try:
            data = json.loads(r_response.text)
        except json.JSONDecodeError as e:
            logger.error(f'Json Decoded Error: {e}')
            raise e
        if data['content']:
            l_filter_data = [match for match in data['content']
                             if match['id'] not in d_matches['ids']]
            l_ids = [resource['id'] for resource in l_filter_data]
            if l_filter_data:
                # Convert JSON to Arrow Table
                s_local_file = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_size_{d_params["size"]}_page_{d_params["page"]}.parquet'
                pa_table = pa.Table.from_pylist(l_filter_data)
                pq.write_table(pa_table, f'/tmp/{s_local_file}')

                # Upload the file to the destination bucket
                client_gcs = GCSClient(gcp_project_id, gcp_conn_id)
                client_gcs.upload_file(
                    bucket_name=gcs_bucket,
                    source_file=f'/tmp/{s_local_file}',
                    destination_blob_name=f"matches_list/date={date.today().strftime('%Y-%m-%d')}/{s_local_file}"
                )
                # Change page if all elements have been readed
                if data['numberOfElements'] == data['size']:
                    d_matches['page'] = d_matches['page'] + 1
                d_matches['ids'] = d_matches['ids'] + l_ids
                fs_client.add_or_update_document(
                    collection_name='padel_intelligence',
                    doc_id='matches_list',
                    data=d_matches
                )
                b_is_new_data = True
            else:
                logger.info('There are not NEW Matches, waiting for...')
                break
    return b_is_new_data


def operator_pi_get_match_stats2gcs(
    gcp_project_id: str,
    gcp_conn_id: str,
    gcs_bucket: str,
    stats_type: str
):
    """
    Function that makes requests to the API of padel intelligence with the created client and then ingests
    the data in GCS, also manages the offset of the API,
    in this case through a page and id with Google Firestore.

    :param gcp_project_id: GCP project ID
    :param gcp_conn_id: Airflow connection ID to connect to GCP
    :param gcs_bucket: Target GCS bucket
    :param stats_type: Stats type to get info of any match

    """
    # Create unique bucket by environment
    gcs_bucket = f'{gcp_project_id.split("-")[0]}_{gcs_bucket}'
    # Get all matches ids
    fs_client = FirestoreClient(gcp_project_id, gcp_conn_id)

    d_matches = fs_client.get_document(
        collection_name='padel_intelligence',
        doc_id='matches_list'
    )
    l_matches_ids = []
    if d_matches:
        l_matches_ids = d_matches['ids']

    # Get stats matches processed
    d_stats_type = fs_client.get_document(
        collection_name='padel_intelligence',
        doc_id=f'matches_stats_{stats_type or "resume"}'
    )
    if d_stats_type:
        l_matches_ids = [
            s_id for s_id in l_matches_ids if s_id not in d_stats_type['ids']]
    else:
        d_stats_type = {'ids': []}
    l_stats_type_ids = d_stats_type['ids']
    if l_matches_ids:
        for id in l_matches_ids:
            try:
                l_stats_info = manage_stats_requests(id, stats_type)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    logger.warning(
                        f'There are not more data for this match: {id}')
                    break
                else:
                    raise e
            # Load to GCS if there are stats
            if l_stats_info:
                # Convert JSON to Arrow Table
                s_local_file = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_match_{id}_{stats_type or "resume"}.parquet'
                pa_table = pa.Table.from_pylist(l_stats_info)
                pq.write_table(pa_table, f'/tmp/{s_local_file}')
                # Upload the file to the destination bucket
                client_gcs = GCSClient(gcp_project_id, gcp_conn_id)

                client_gcs.upload_file(
                    bucket_name=gcs_bucket,
                    source_file=f'/tmp/{s_local_file}',
                    destination_blob_name=f"matches_stats_{stats_type or 'resume'}/date={date.today().strftime('%Y-%m-%d')}/{s_local_file}"
                )
            # Add new control ids
            l_stats_type_ids.append(id)
            d_stats_type['ids'] = l_stats_type_ids
            fs_client.add_or_update_document(
                collection_name='padel_intelligence',
                doc_id=f'matches_stats_{stats_type or "resume"}',
                data=d_stats_type
            )
    else:
        logger.info('There are not NEW Matches, waiting for...')
