import os
import logging
from langchain.schema import HumanMessage, SystemMessage

from integrations.custom_prompts.prompt_loader import load_prompts
from typing import Optional, Dict, Any, cast
from utils.get_chat_model import get_chat_model
from utils.chat_models import CHAT_MODELS
from utils.get_logger import CustomLogger

openai_api_key = os.getenv("OPENAI_API_KEY")
logger = CustomLogger(module_name=__name__)


def convert_json_to_text(
    user_input: str,
    api_response: str,
    api_request_data: Dict[str, Any],
    bot_id: str,
) -> str:
    chat = get_chat_model(CHAT_MODELS.gpt_3_5_turbo_16k)

    api_summarizer_template = None
    system_message = SystemMessage(
        content="You are a chatbot that can understand API responses"
    )
    prompt_templates = load_prompts(bot_id)
    api_summarizer_template = (
        prompt_templates.api_summarizer if prompt_templates else None
    )

    if api_summarizer_template is not None:
        system_message = SystemMessage(content=api_summarizer_template)

    messages = [
        system_message,
        HumanMessage(
            content="You'll receive user input and server responses obtained by making calls to various APIs. You will also recieve a dictionary that specifies, the body, param and query param used to make those api calls. Your task is to transform the JSON response into a response that in an answer to the user input. You should inform the user about the filters that were used to make these api calls"
        ),
        HumanMessage(content=f"Here is the user input: {user_input}."),
        HumanMessage(
            content=f"Here is the response from the apis: {api_response}"
        ),
        HumanMessage(
            content=f"Here is the api_request_data: {api_request_data}"
        ),
    ]

    result = chat(messages)
    logger.info("Convert json to text", content=result.content, incident="convert_json_to_text", api_request_data=api_request_data)

    return cast(str, result.content)
