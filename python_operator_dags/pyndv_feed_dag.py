"""Example DAG demonstrating the usage of the PythonOperator with pyndv."""

import json
import time
from pathlib import Path

import pymongo
from airflow.models import DAG
from airflow.models import Variable as var
from airflow.operators.python_operator import (PythonOperator,
                                               PythonVirtualenvOperator)
from airflow.utils.dates import datetime, timedelta
from pyndv import core

PYNDV_OUTPUT_FILE = "./pyndv_output.json"


def pyndv_write_feed(user_name, user_password, server_uri):
    """pyndv_write_feed [summary]
    
    [extended_summary]
    
    Args:
        user_name ([type]): [description]
        user_password ([type]): [description]
        server_uri ([type]): [description]
    """
    try:
        with open(PYNDV_OUTPUT_FILE) as ndv_file:
            data = json.load(ndv_file)
        server_conection_string = (
            f"mongodb+srv://{user_name}:{user_password}@{server_uri}"
        )
        with pymongo.MongoClient(server_conection_string) as client:
            db = client.get_database("pyndvdb")
            col = db.get_collection("pyndv_feeds")
            col.insert_one(data)
    except Exception as ex:
        print(ex)
        exit(1)


def write_failure_callback():
    """write_failure_callback [summary]
    
    [extended_summary]
    """
    print("write_failure_callback")


def write_success_callback(success):
    """write_success_callback [summary]
    
    [extended_summary]
    
    Args:
        success ([type]): [description]
    """
    print(f"write_success_callback {success}")
    import os

    try:
        os.remove(PYNDV_OUTPUT_FILE)
    except OSError as os_error:
        print(os_error)
        exit(1)


def write_retry_callback():
    """write_retry_callback [summary]
    
    [extended_summary]
    """
    print("write_retry_callback")


def pyndv_download():
    """pyndv_download [summary]
    
    [extended_summary]
    
    Returns:
        [type]: [description]
    """
    feed_processor = core.FeedProcessor()
    feed_processor(feed_type=None, output=PYNDV_OUTPUT_FILE)

default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 1, 31),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="pyndv_feed", default_args=default_args, schedule_interval="@daily", catchup=False
)

download_feed = PythonOperator(
    task_id="pyndv_download_feed", python_callable=pyndv_download, dag=dag
)

write_feed = PythonOperator(
    task_id="pyndv_write_feed",
    python_callable=pyndv_write_feed,
    op_args=[
        var.get("mlab_user_name"),
        var.get("mlab_user_password"),
        var.get("mlab_server_uri"),
    ],
    on_failure_callback=write_failure_callback,
    on_retry_callback=write_retry_callback,
    on_success_callback=write_success_callback,
    wait_for_downstream=True,
    dag=dag,
)

download_feed >> write_feed
