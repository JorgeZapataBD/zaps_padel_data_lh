import logging
import os
from datetime import date, datetime
from typing import Literal

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from pypdf import PdfReader
from zaps_core.clients.firestore_client import FirestoreClient
from zaps_core.clients.gcs_client import GCSClient

from plugins.zaps_padel.utils.utils_ranking_fip import (
    download_ranking_fip_file, format_ranking_fip_header, get_mondays_list,
    get_ranking_fip_pattern)

logger = logging.getLogger(__name__)


def operator_get_ranking_fip_files2gcs(
    gcp_project_id: str,
    gcp_conn_id: str,
    gcs_bucket: str,
    fip_category: Literal["Male", "Female", 'Race-Male', 'Race-Female'],
    init_date: date = datetime.strptime('2023-09-01', '%Y-%m-%d').date()
):
    """
    Function that downloads ranking files from the official International Padel Federation (FIP) website
    from a given start date until the current date and saves them to GCS. Additionally, it marks the last
    processed file date to avoid re-reading it.

    :param gcp_project_id: GCP project ID (str)
    :param gcp_conn_id: Airflow connection ID to connect to GCP (str)
    :param gcs_bucket: Target GCS bucket (str)
    :param fip_category: FIP category, currently available for Male and Female (str)
    :param init_date: Initial download date, it will only be used if no previous date is marked (date)
    :return: Bool that define if any file has been ingested
    """
    # Bool to define if there is new data
    b_is_new_data = False
    # Create unique bucket by environment
    gcs_bucket = f'{gcp_project_id.split("-")[0]}_{gcs_bucket}'
    # Check if a last read date is already marked in Firestore, if so, replace init_date
    client_fs = FirestoreClient(gcp_project_id, gcp_conn_id)

    last_date = client_fs.get_document(
        collection_name='fip_ranking',
        doc_id=fip_category
    )
    if last_date:
        init_date = datetime.strptime(
            last_date['last_date'], '%Y-%m-%d').date()

    # Get all Mondays from the given date to check if there are files for those weeks
    dates_list = get_mondays_list(init_date)
    if dates_list:
        for d_date in dates_list:
            # If no file is found for a date, continue and mark the date (not all weeks update the ranking)
            try:
                source_file = download_ranking_fip_file(d_date, fip_category)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    logger.warning(
                        f"No Ranking update for the date: {d_date.strftime('%Y-%m-%d')}")
                    continue
                else:
                    raise e
            except Exception as e:
                raise e

            # Create the GCS client
            client_gcs = GCSClient(gcp_project_id, gcp_conn_id)
            client_gcs.upload_file(
                bucket_name=gcs_bucket,
                source_file=source_file,
                destination_blob_name=f"{fip_category}/{d_date.today().strftime('%Y-%m-%d')}/{source_file}",
            )
            # Update the last processed date
            client_fs.add_or_update_document(
                collection_name='fip_ranking',
                doc_id=fip_category,
                data={"last_date": date.strftime('%Y-%m-%d')}
            )
            b_is_new_data = True
    else:
        logger.info("Waiting for the next week's file")
    return b_is_new_data


def operator_parser_ranking_fip_files_gcs2gcs(
    gcp_project_id: str,
    gcp_conn_id: str,
    gcs_src_bucket: str,
    gcs_dst_bucket: str,
    gcs_prefix: str,
    fip_category: str,
    pages: int
):
    """
    Downloads PDF files from GCS, normalizes them, and uploads them back to GCS in Parquet format.
    Due to differences in files, parsing logic must be added depending on the header.

    :param gcp_project_id: GCP project ID
    :param gcp_conn_id: Airflow connection ID to connect to GCP
    :param gcs_src_bucket: GCS source bucket
    :param gcs_dst_bucket: GCS destination bucket
    :param gcs_prefix: Prefix to filter GCS files
    :param fip_category: Category and ranking type
    :param pages: Number of pages to read from the PDF file
    """
    # Create unique bucket by environment
    gcs_src_bucket = f'{gcp_project_id.split("-")[0]}_{gcs_src_bucket}'
    gcs_dst_bucket = f'{gcp_project_id.split("-")[0]}_{gcs_dst_bucket}'

    # Generate a list of files and select only PDFs to avoid folder paths
    client_gcs = GCSClient(gcp_project_id, gcp_conn_id)
    l_files = client_gcs.list_files(
        bucket_name=gcs_src_bucket,
        prefix=f'{fip_category}/{gcs_prefix}'
    )
    l_files = [file for file in l_files if file.endswith('.pdf')]
    # Download the files, process them, and then remove them (Also saved in /tmp for automatic deletion if there's a failure)
    for f_blob in l_files:
        local_file = f"/tmp/{f_blob.split('/')[-1]}"
        client_gcs.download_file(
            bucket_name=gcs_src_bucket,
            blob_name=f_blob,
            local_file_path=local_file
        )
        # Read PDF files using pypdf
        reader = PdfReader(local_file)
        os.remove(local_file)
        # Extract the text content into a list of lines
        text = ''
        for i in range(min(pages, len(reader.pages))):
            page = reader.pages[i]
            text += page.extract_text() + '\n'
        # Modify the encoding since there are Spanish names (accents, ñ...)
        text = text.encode('latin1', 'ignore').decode('utf-8', "ignore")
        lines = text.split("\n")
        lines = [line for line in text.split("\n") if line.strip()]
        # Check if the file can be parsed, if not continue with the next one
        l_header = format_ranking_fip_header(lines[0])
        pattern = get_ranking_fip_pattern(l_header)
        if not pattern:
            logger.error(f"Error header Not Controlled for File: {f_blob}")
            continue
        try:
            # Parse the file
            parsed_data = []
            for line in lines[1:-1]:
                match = pattern.match(line)
                data = {}
                data['ranking_date'] = datetime.strptime(
                    f_blob.split('/')[-1].split('_')[0], '%Y-%m-%d').date()
                data['position'] = int(match.group('position'))
                data['player'] = match.group('player').strip()
                if 'country' in match.groupdict():
                    data['country'] = match.group('country')
                data['points'] = int(match.group('points'))
                parsed_data.append(data)
        except Exception as e:
            logger.error(f"Error parsing File {f_blob}: {e}")
            continue

        # Convert JSON to Arrow Table
        table = pa.Table.from_pylist(parsed_data)
        # Save as Parquet
        pq.write_table(table, local_file.replace('.pdf', '.parquet'))

        # Upload the file to the destination bucket
        client_gcs.upload_file(
            bucket_name=gcs_dst_bucket,
            source_file=local_file.replace('.pdf', '.parquet'),
            destination_blob_name=f"{fip_category}/date={date.today().strftime('%Y-%m-%d')}/{f_blob.split('/')[-1].replace('.pdf', '.parquet')}"
        )
