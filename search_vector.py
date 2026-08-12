from openai import AzureOpenAI
import requests
import os

# ---------- Azure AI / Embedding ----------

client = AzureOpenAI(
    azure_endpoint="https://ai-agents-project64121704-resource.services.ai.azure.com",
    api_key=os.environ["AZURE_AI_API_KEY"],
    api_version="2024-10-21"
)

query = "How do I recover a 502 error in India production?"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_vector = response.data[0].embedding

print("Query:", query)
print("Query vector dimensions:", len(query_vector))


# ---------- Azure AI Search ----------

search_endpoint = "https://ai-search64121704.search.windows.net"
search_api_key = os.environ["SEARCH_API_KEY"]

url = (
    f"{search_endpoint}/indexes/incident-knowledge/docs/search"
    f"?api-version=2025-09-01"
)

headers = {
    "Content-Type": "application/json",
    "api-key": search_api_key
}

search_body = {
    "vectorQueries": [
        {
            "kind": "vector",
            "vector": query_vector,
            "fields": "contentVector",
            "k": 3
        }
    ],
    "filter": "region eq 'India'",
    "search": "502 error India production",
    "select": "id,content,alertType,severity,region,documentVersion"
}

search_response = requests.post(
    url,
    headers=headers,
    json=search_body
)

print("\nSearch status:", search_response.status_code)
print(search_response.text)