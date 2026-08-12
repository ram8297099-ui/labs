from openai import AzureOpenAI

endpoint = "https://ai-agents-project64121704-resource.services.ai.azure.com"
api_key = "bd677dbbf87841049dccbf4bce49e5d1"

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version = "2024-10-21"
)

response = client.embeddings.create(
    model = "text-embedding-3-small",
    input = "Restart the unhealthy Kubernetes pod after saturation."
)

embedding = response.data[0].embedding

print("Vector dimensions:", len(embedding))
print("First 10 values:", embedding[:10])