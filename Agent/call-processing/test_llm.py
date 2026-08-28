import logging

from llm_client import authenticate, ask_llm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

# Hide Azure/OpenAI SDK internal logs
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logging.info("911 incident investigation started")

prompt = """
You are investigating a simulated 911 call-processing application.

Pod status:
Running
Ready: true
Restarts: 0

CPU:
0.075 cores

Memory:
9312 Ki

Application logs:
ERROR Database connection timeout
ERROR [Errno 111] Connection refused

What is the most likely area to investigate next?
Give a concise explanation.
"""


authenticate()

result = ask_llm(prompt)

logging.info("FINAL LLM RESPONSE:")
print()
print(result)
print()

logging.info("911 incident investigation completed")