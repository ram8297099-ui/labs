import os
import json

from openai import (
    OpenAI,
    APIError,
    APIConnectionError,
    NotFoundError,
)

from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider,
)

from tools import (
    get_service,
    get_service_endpoints,
    check_tcp_connectivity,
)


AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


credential = DefaultAzureCredential()

token_provider = get_bearer_token_provider(
    credential,
    "https://ai.azure.com/.default",
)


client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT.rstrip("/") + "/openai/v1",
    api_key=token_provider,
)


TOOLS = [
    {
        "type": "function",
        "name": "get_service",
        "description": "Get Kubernetes Service configuration.",
        "parameters": {
            "type": "object",
            "properties": {
                "namespace": {
                    "type": "string"
                },
                "service_name": {
                    "type": "string"
                },
            },
            "required": [
                "namespace",
                "service_name",
            ],
        },
    },

    {
        "type": "function",
        "name": "get_service_endpoints",
        "description": "Get the endpoints behind a Kubernetes Service.",
        "parameters": {
            "type": "object",
            "properties": {
                "namespace": {
                    "type": "string"
                },
                "service_name": {
                    "type": "string"
                },
            },
            "required": [
                "namespace",
                "service_name",
            ],
        },
    },

    {
        "type": "function",
        "name": "check_tcp_connectivity",
        "description": "Test TCP connectivity from an application pod to a host and port.",
        "parameters": {
            "type": "object",
            "properties": {
                "namespace": {
                    "type": "string"
                },
                "pod_name": {
                    "type": "string"
                },
                "host": {
                    "type": "string"
                },
                "port": {
                    "type": "integer"
                },
            },
            "required": [
                "namespace",
                "pod_name",
                "host",
                "port",
            ],
        },
    },
]


def execute_tool(name, arguments):

    if name == "get_service":
        return get_service(**arguments)

    if name == "get_service_endpoints":
        return get_service_endpoints(**arguments)

    if name == "check_tcp_connectivity":
        return check_tcp_connectivity(**arguments)

    return {
        "error": f"Unknown tool: {name}"
    }


def analyze_incident(status, logs, metrics):

    prompt = f"""
You are an incident investigation agent for a production
911 call-processing platform.

Initial evidence:

SERVICE STATUS:
{json.dumps(status, indent=2)}

RESOURCE METRICS:
{json.dumps(metrics, indent=2)}

APPLICATION LOGS:
{logs}

Investigate the incident.

You have Kubernetes diagnostic tools available.
Use them when additional evidence is required.

Do not assume the root cause.
Do not invent evidence.

At the end provide:

1. Most likely failure area
2. Evidence supporting the conclusion
3. Recommended next investigation step
"""

    try:

        print("\n[LLM] Sending investigation request")
        print(f"[LLM] Endpoint   : {AZURE_OPENAI_ENDPOINT}")
        print(f"[LLM] Deployment : {AZURE_OPENAI_DEPLOYMENT}")

        # Keep the complete conversation state
        input_items = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        response = client.responses.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            input=input_items,
            tools=TOOLS,
        )

        while True:

            # Preserve the model's response items
            input_items.extend(response.output)

            tool_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            # No more tools required
            if not tool_calls:
                break

            for tool_call in tool_calls:

                arguments = json.loads(
                    tool_call.arguments
                )

                print(
                    f"\n[AI TOOL CALL] {tool_call.name}"
                )

                print(
                    f"[ARGUMENTS] {arguments}"
                )

                result = execute_tool(
                    tool_call.name,
                    arguments,
                )

                print(
                    f"[TOOL RESULT] {result}"
                )

                # Add tool result to conversation
                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": json.dumps(result),
                    }
                )

            # Send complete state back to Azure OpenAI
            response = client.responses.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                input=input_items,
                tools=TOOLS,
            )

        print("\n[LLM] Response received")

        return response.output_text


    except NotFoundError as e:

        print("\n[AI ERROR]")
        print("Azure OpenAI request failed")
        print(f"Endpoint   : {AZURE_OPENAI_ENDPOINT}")
        print(f"Deployment : {AZURE_OPENAI_DEPLOYMENT}")
        print(f"Details    : {e}")

        return (
            "AI analysis is currently unavailable. "
            "The configured Azure OpenAI resource or deployment "
            "could not be found."
        )


    except APIConnectionError as e:

        print("\n[AI ERROR]")
        print("Unable to connect to Azure OpenAI")
        print(f"Endpoint   : {AZURE_OPENAI_ENDPOINT}")
        print(f"Deployment : {AZURE_OPENAI_DEPLOYMENT}")
        print(f"Details    : {e}")

        return (
            "AI analysis is currently unavailable because "
            "Azure OpenAI could not be reached."
        )


    except APIError as e:

        print("\n[AI ERROR]")
        print("Azure OpenAI API error")
        print(f"Endpoint   : {AZURE_OPENAI_ENDPOINT}")
        print(f"Deployment : {AZURE_OPENAI_DEPLOYMENT}")
        print(f"Details    : {e}")

        return (
            "AI analysis is currently unavailable because "
            "Azure OpenAI returned an API error."
        )