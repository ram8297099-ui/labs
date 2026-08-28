from openai import AzureOpenAI
import os
import requests

endpoint = "https://ai-agents-project64121704-resource.services.ai.azure.com"
api_key = os.environ["AZURE_AI_API_KEY"]

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-10-21"
)

incident_text = """
HTTP 502 errors in the India production environment may occur
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

search_url = (
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
            "id": "irp-502-india-001",
            "content": incident_text,
            "contentVector": embedding,
            "alertType": "HTTP502",
            "severity": "Sev0",
            "region": "India",
            "documentVersion": "v1"
        }
    ]
}

search_response = requests.post(
    search_url,
    headers=headers,
    json=document
)

print("Search status:", search_response.status_code)
print(search_response.text)
print("Incident text:")
print(incident_text)

print("Vector dimensions:", len(embedding))
print("First 10 vector values:", embedding[:10])