from openai import OpenAI
import os


client = OpenAI(
    api_key=os.environ["AZURE_AI_API_KEY"],
    base_url=os.environ["AZURE_AI_ENDPOINT"]
)


user_query = "How do I recover a 502 error in India production?"


retrieved_context = """
HTTP 502 errors in the India production environment are currently
handled by first validating Application Gateway backend health and
pod readiness. If the backend pod is unhealthy, follow the approved
rolling restart procedure and verify application health before
closing the incident.
"""


system_prompt = """
You are a 911 incident response assistant.

Use the supplied incident knowledge to answer the user's question.

Rules:
1. Use the retrieved context as the primary source of truth.
2. Do not invent remediation procedures.
3. If the context does not contain enough information, clearly say
   that the available incident knowledge is insufficient.
4. Keep the response concise and operationally useful.
"""


user_prompt = f"""
Retrieved incident knowledge:

{retrieved_context}

User question:

{user_query}
"""


response = client.responses.create(
    model="gpt-5.1",
    instructions=system_prompt,
    input=user_prompt
)


answer = response.output_text

print("\nAnswer:\n")
print(answer)