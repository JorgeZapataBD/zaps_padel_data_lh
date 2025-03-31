from zaps_core.clients.bigquery_client import BigQueryClient


def operator_create_external_table(
    gcp_project_id: str,
    gcp_conn_id: str,
    gcs_bucket: str,
    gcs_prefix: str,
    bq_dataset_id: str,
    bq_table_id: str
):
    """
    Function that create external table if not exist

    :param gcp_project_id: GCP project ID
    :param gcp_conn_id: Airflow connection ID to connect to GCP
    :param gcs_bucket: Origin GCS bucket
    :param gcs_prefix: GCS prefix to create table
    :param bq_dataset_id: Target BigQuery Dataset
    :param bq_table_id: Bigquery table
    """
    # Create unique bucket by environment
    gcs_bucket = f'{gcp_project_id.split("-")[0]}_{gcs_bucket}'
    # Query to create external table with hive partition filter
    query = f"""
        CREATE EXTERNAL TABLE {bq_dataset_id}.{bq_table_id}
        WITH PARTITION COLUMNS
        OPTIONS (
        uris = ['gs://{gcs_bucket}/{gcs_prefix}/*.parquet'],
        format = 'PARQUET',
        hive_partition_uri_prefix = 'gs://{gcs_bucket}/{gcs_prefix}',
        require_hive_partition_filter = true)
    """
    # Create table if not exists
    bq_client = BigQueryClient(gcp_project_id, gcp_conn_id)
    if not bq_client.check_table_exists(bq_dataset_id, bq_table_id):
        bq_client.execute_query(query)
