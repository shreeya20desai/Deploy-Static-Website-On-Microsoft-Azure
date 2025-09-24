import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient

# Cosmos DB configuration
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
DATABASE_NAME = "ResumeDB"
CONTAINER_NAME = "Visitors"

# Initialize Cosmos client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Read the document with id "1"
        doc = container.read_item(item="1", partition_key="1")

        # Ensure 'visit' is treated as an integer
        current_visit = int(doc.get("visit", 0))
        doc["visit"] = current_visit + 1

        # Update the document in Cosmos DB
        container.upsert_item(doc)

        return func.HttpResponse(
            f"Visitor count: {doc['visit']}",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error updating visitor count: {e}")
        return func.HttpResponse(
            f"Internal server error: {str(e)}",
            status_code=500
        )
