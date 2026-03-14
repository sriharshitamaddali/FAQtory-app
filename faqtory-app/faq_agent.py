from langchain.agents import create_agent
from claude_model import initialise_model
from tools import retrieve_data_for_faqs
from prompt_generator import generate_system_prompt

def create_faq_agent():
    """
    Creates an agent that generates FAQs in markdown format based on a given document 
    and audience sections.
    The agent uses the ClaudeModel to process the document and generate FAQs, 
    and the retrieve_data_for_faqs tool to extract relevant content from the document based on 
    the specified audience sections.
    """
    claude_agent = initialise_model()

    task = "read and understand the given document and generate the FAQs in markdown format." \
    "Your job is to analyse documents and create comprehensive FAQs for specific audience.  " \
    "Provide the FAQs audience section wise. The tone of the FAQs should be formal"

    system_prompt = generate_system_prompt(
        role="Content Writer",
        task=task
    )

    agent = create_agent(
        model=claude_agent,
        tools=[retrieve_data_for_faqs],
        system_prompt=system_prompt
    )

    return agent
