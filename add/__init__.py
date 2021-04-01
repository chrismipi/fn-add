import uuid
import os
from dotenv import load_dotenv
load_dotenv()

import logging
import azure.functions as func
from azure.cosmos import CosmosClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    uid = uuid.uuid4()

    url = os.environ['ACCOUNT_URI']
    key = os.environ['ACCOUNT_KEY']
    client = CosmosClient(url, credential=key)
    database_name = 'ToDoDB'
    database = client.get_database_client(database_name)
    container_name = 'Actions'
    container = database.get_container_client(container_name)

    try:
        req_body = req.get_json()
        title = req_body.get('title')

        container.upsert_item({
            'id': str(uid),
            'title': title,
            'location': 'SouthAfrica',
            'complete': False
        })

        return func.HttpResponse(
            "Saved",
            status_code=201
        )

    except Exception:
        return func.HttpResponse("Error", status_code=500)