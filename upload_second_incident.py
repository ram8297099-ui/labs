from openai import AzureOpenAI
import requests
import os

client = AzureOpenAI(
    azure_endpoint="https://ai-agents-project64121704-resource.services.ai.azure.com",
    api_key=os.environ["AZURE_AI_API_KEY"],
    api_version="2024-10-21"
)

incident_text = """
HTTP 502 errors in the United States production environment may occur
when the Application Gateway cannot reach a healthy backend pod.
Verify backend health and pod readiness before performing remediation.
"""

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=incident_text
)

embedding = response.data[0].embedding

search_endpoint = "https://ai-search64121704.search.windows.net"
search_api_key = os.environ["SEARCH_API_KEY"]

url = (
    f"{search_endpoint}/indexes/incident-knowledge/docs/index"
    f"?api-version=2025-09-01"
)

headers = {
    "Content-Type": "application/json",
    "api-key": search_api_key
}

document = {
    "value": [
        {
            "@search.action": "upload",
            "id": "irp-502-us-001",
            "content": incident_text,
            "contentVector": embedding,
            "alertType": "HTTP502",
            "severity": "Sev0",
            "region": "US",
            "documentVersion": "v1"
        }
    ]
}

response = requests.post(
    url,
    headers=headers,
    json=document
)

print("Status:", response.status_code)
print(response.text)