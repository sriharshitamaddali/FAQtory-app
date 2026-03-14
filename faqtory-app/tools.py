from langchain.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import PDFDocumentLoader
from embeddings import Embeddings
from langchain_chroma import Chroma
import chromadb
from chromadb.config import Settings


@tool
def retrieve_data_for_faqs(
    audience: list[str],
    path: str
) -> str:
    """
    This tool retrieves relevant content from a PDF document based on the specified audience sections. 
    Args:
    - audience (dict): A dictionary specifying the audience sections for which FAQs need to be generated.
    - path (str): The file path to the PDF document from which content needs to be extracted.
    It performs the following steps:
        1. Extracts text from the PDF document using the PDFDocumentLoader.
        2. Splits the extracted document into manageable chunks using RecursiveCharacterTextSplitter.
        3. Initializes an embedding model to convert the text chunks into vector representations.
        4. Stores the embeddings in a Chroma vector database for efficient retrieval.
        5. Retrieves relevant chunks from the vector database based on the audience sections specified in the query.
        6. Formats the retrieved chunks into a markdown format suitable for generating FAQs.
    """
    #Step 1: Extract text from the PDF document
    pdf_loader = PDFDocumentLoader(path)
    extracted_data = pdf_loader.extract_text_from_file()
    # print("Extracted data from PDF:", extracted_data)

    #TO-DO: Validate the checksum
    #Apply text sanitization and preprocessing here to clean the extracted text data, remove any unwanted characters, normalize whitespace, and ensure the text is in a consistent format for further processing.
    #Add readaction layer here to redact any PII or PHI info

    #Step 2: Split the document into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # for doc in extracted_data:
    chunks = splitter.split_documents(extracted_data)
    # print("Document split into chunks:", chunks)

    #Step 3: Initilise the embedding model
    embeddings = Embeddings().initialize_embeddings()

    # batch_embeddings = BatchEmbeddingWithRateLimit(
    #     embeddings_model=embeddings,
    #     batch_size=20,
    #     delay=30
    # )

    #Step 4: Store the embeddings in vector DB -- initiliase the chroma DB vector store and configure the embeddings, collection, storage path 
    #initialise the chroma DB client
    chromadb_client = chromadb.Client(
        Settings(
            chroma_server_host=None,        # Ensures pure in-memory mode
            chroma_server_http_port=None,   # No server port
            telemetry_enabled=False         # Disables telemetry
        )
    )
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="faq_documents",
        client=chromadb_client,
    )

    #Step 5: Add_documents will add all the split documents(convert into embeddings) and stroe in vector DB
    # vector_store.add_documents(documents=chunks)

    #Step 6: Send the retrieved chunks to the Claude model to generate FAQs in markdown format
    role_query = f"Extract content relevant for the following audience sections: {audience}"
    retrieved_docs = vector_store.similarity_search(role_query.format(audience=audience), k=5)

    #Format retrieved documents
    formatted_docs = []
    i = 1
    for doc in retrieved_docs:
        formatted_docs.append(
            f"## Source {i}:\n{doc.page_content}\n"
        )
        i += 1

    formatted_results = "\n----\n".join(formatted_docs)

    return formatted_results