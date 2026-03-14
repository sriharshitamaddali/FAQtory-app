import logging
from faq_agent import create_faq_agent
from langchain.messages import HumanMessage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

def generate_faqs(audience: list[str], path: str) -> str:
    # Here you would implement the logic to generate FAQs based on the document and audience
    # For demonstration purposes, we'll return a placeholder string
    agent = create_faq_agent()

    user_message = f"As a content writer, analyse the document in this path {path}. Generate FAQs based on the document for the following audience sections: {audience}"

    result = agent.invoke({
        "messages": [
            HumanMessage(content=user_message)
        ]
    })

    messages = result.get('messages', [])
    if messages and len(messages) > 1:
        faqs = messages[-1].content
        logger.info("Final response from Claude model: %s", faqs)

    return faqs

if __name__ == "__main__":
    audience = [
        "High school students",
        "Educational counselors"
    ]

    path = "./sat-school-day-student-guide.pdf"

    result = generate_faqs(audience, path=path)

    with(open("generated_faqs.md", "w") as faq_file):
        faq_file.write(result)

    print("Generated FAQs in markdown format:", result)