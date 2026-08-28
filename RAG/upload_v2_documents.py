from openai import AzureOpenAI
import requests
import os

AI_ENDPOINT = "https://ai-agents-project64121704-resource.services.ai.azure.com"
SEARCH_ENDPOINT = "https://ai-search64121704.search.windows.net"

client = AzureOpenAI(
    azure_endpoint=AI_ENDPOINT,
    api_key=os.environ["AZURE_AI_API_KEY"],
    api_version="2024-10-21"
)

documents = [
    {
        "id": "irp-502-india-v1",
        "content": """
HTTP 502 errors in the India production environment may occur
when the Application Gateway cannot reach a healthy backend pod.
Verify backend health and pod readiness before performing remediation.
""",
        "region": "India",
        "isActive": False,
        "version": "v1"
    },
    {
        "id": "irp-502-india-v2",
        "content": """
HTTP 502 errors in the India production environment are currently
handled by first validating Application Gateway backend health and
pod readiness. If the backend pod is unhealthy, follow the approved
rolling restart procedure and verify application health before
closing the incident.
""",
        "region": "India",
        "isActive": True,
        "version": "v2"
    },
    {
        "id": "irp-502-us-v1",
        "content": """
HTTP 502 errors in the United States production environment may occur
when the Application Gateway cannot reach a healthy backend pod.
Verify backend health and pod readiness before performing remediation.
""",
        "region": "US",
        "isActive": True,
        "version": "v1"
    }
]

search_api_key = os.environ["SEARCH_API_KEY"]

url = (
    f"{SEARCH_ENDPOINT}/indexes/incident-knowledge-v2/docs/index"
    f"?api-version=2025-09-01"
)

headers = {
    "Content-Type": "application/json",
    "api-key": search_api_key
}

search_documents = []

for doc in documents:

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc["content"]
    )

    embedding = response.data[0].embedding

    search_documents.append({
        "@search.action": "upload",
        "id": doc["id"],
        "content": doc["content"],
        "contentVector": embedding,
        "alertType": "HTTP502",
        "severity": "Sev0",
        "region": doc["region"],
        "documentVersion": doc["version"],
        "isActive": doc["isActive"]
    })

payload = {
    "value": search_documents
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print("Status:", response.status_code)
print(response.text)