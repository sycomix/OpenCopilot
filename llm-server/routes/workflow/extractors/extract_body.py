import os
from langchain.schema import HumanMessage, SystemMessage
from utils.chat_models import CHAT_MODELS
from utils.get_chat_model import get_chat_model
from shared.utils.opencopilot_utils import get_llm

from typing import Any, Optional
from routes.workflow.extractors.extract_json import extract_json_payload
import importlib
from utils.get_logger import CustomLogger

logger = CustomLogger(module_name=__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = get_llm()


async def gen_body_from_schema(
    body_schema: str,
    text: str,
    prev_api_response: str,
    app: Optional[str],
    current_state: Optional[str],
) -> Any:
    chat = get_chat_model(CHAT_MODELS.gpt_3_5_turbo_16k)
    api_generation_prompt = None
    if app:
        module_name = f"integrations.custom_prompts.{app}"
        module = importlib.import_module(module_name)
        api_generation_prompt = getattr(module, "api_generation_prompt")

    messages = [
        SystemMessage(
            content="You are an intelligent machine learning model that can produce REST API's body in json format"
        ),
        HumanMessage(
            content="You will be given swagger schema, user input, data from previous api calls, and current state information stored in the current_state variable. You should use the field descriptions provided in the schema to generate the payload."
        ),
        HumanMessage(content=f"Swagger Schema: {body_schema}"),
        HumanMessage(content=f"User input: {text}"),
        HumanMessage(content=f"prev api responses: {prev_api_response}"),
        HumanMessage(content=f"current_state: {current_state}"),
        HumanMessage(
            content="If the user is asking to generate values for some fields, likes product descriptions, jokes etc add them."
        ),
        HumanMessage(
            content="Given the provided information, generate the appropriate minified JSON payload to use as body for the API request. If a user doesn't provide a required parameter, use sensible defaults for required params, and leave optional params."
        ),
    ]

    if api_generation_prompt is not None:
        messages.append(HumanMessage(content=f"{api_generation_prompt}"))

    result = chat(messages)

    logger.info("LLM Body Response", content=result.content, text=text, app=app)

    d: Any = extract_json_payload(result.content)
    logger.info("Parsed the json payload", payload=d, app=app, api_generation_prompt=api_generation_prompt)

    return d
