import os
import requests

SEARCH_ENDPOINT = "https://ai-search64121704.search.windows.net"
SEARCH_API_KEY = os.environ["SEARCH_API_KEY"]

INDEX_NAME = "incident-knowledge"

url = f"{SEARCH_ENDPOINT}/indexes/{INDEX_NAME}?api-version=2025-09-01"

headers = {
    "Content-Type": "application/json",
    "api-key": SEARCH_API_KEY,
}

index_definition = {
    "name": INDEX_NAME,
    "fields": [
        {
            "name": "id",
            "type": "Edm.String",
            "key": True,
            "searchable": False,
            "filterable": True
        },
        {
            "name": "content",
            "type": "Edm.String",
            "searchable": True
        },
        {
            "name": "contentVector",
            "type": "Collection(Edm.Single)",
            "searchable": True,
            "dimensions": 1536,
            "vectorSearchProfile": "vector-profile"
        },
        {
            "name": "alertType",
            "type": "Edm.String",
            "filterable": True
        },
        {
            "name": "severity",
            "type": "Edm.String",
            "filterable": True
        },
        {
            "name": "region",
            "type": "Edm.String",
            "filterable": True
        },
        {
            "name": "documentVersion",
            "type": "Edm.String",
            "filterable": True
        }
    ],
    "vectorSearch": {
        "algorithms": [
            {
                "name": "hnsw-algorithm",
                "kind": "hnsw"
            }
        ],
        "profiles": [
            {
                "name": "vector-profile",
                "algorithm": "hnsw-algorithm"
            }
        ]
    }
}

response = requests.put(
    url,
    headers=headers,
    json=index_definition
)

print("Status:", response.status_code)
print(response.text)