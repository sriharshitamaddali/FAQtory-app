from langchain_anthropic.chat_models import ChatAnthropic
import logging
from config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# class ClaudeModel:
#     def __init__(self):
def initialise_model():
    model = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature=0,
        api_key=settings.secrets["anthropic_api_key"],
        timeout=45
    )   
    logger.info("Initialized ChatAnthropic model.")

    return model
