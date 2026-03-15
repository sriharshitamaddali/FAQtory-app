# FAQtory-app

## About
FAQ Engine is a Retrieval-Augmented Generation (RAG) based application that allows users to upload a PDF document and automatically generate FAQs tailored to a specific target audience.
 
Users interact via a UI where they upload a PDF and select their intended audience (e.g. Technical, Executive, Non-Technical). The application then processes the document through a secure ingestion pipeline and leverages a LangChain-powered RAG pipeline backed by an LLM (Claude / OpenAI) to generate relevant, audience-specific FAQs.

---
 
## Background
 
The FAQ Engine is part of a larger document processing pipeline. The broader system handles:
 
- **File Upload & Security** — User uploads PDF via UI, stored in an S3 Upload Bucket
- **Malware Scanning** — File is scanned before being moved to a secure S3 bucket
- **Invocation** — An S3 PUT event triggers a Lambda function which invokes the FAQ Engine on ECS
 
This repository contains **only the FAQ Engine**. The surrounding infrastructure (S3, Lambda, ECS, UI) is managed separately.
 
---


## How it works

### FAQ Engine Flow
![FAQ Engine Architecture](faqtory-engine.png)

The FAQ Engine runs as a sequential LangChain pipeline:
 
1. PDF is loaded using `OpenDataLoader PDFLoader`
2. Text is extracted and split into chunks using **Recursive Text Splitter**
3. Chunks are encoded into embeddings and stored in **Chroma DB** (in-memory vector store)
4. A fixed query is run against Chroma DB to retrieve chunks relevant to the selected audience
5. Retrieved chunks are combined with a **System Prompt** and the selected **Audience** to build the final prompt
6. Prompt is sent to the **LLM** (Claude / OpenAI)
7. LLM returns generated FAQs tailored to the selected audience

## Tech Stack
 
| Component | Technology |
|---|---|
| Backend / Pipeline | Python, LangChain |
| LLM | Claude / OpenAI (configurable) |
| Vector Store | Chroma DB (in-memory, switchable to FAISS) |
| Embeddings | OpenAI Embeddings |
| PDF Loader | OpenDataLoader PDFLoader |

## Upcoming / Planned Changes
 
- [ ] Apply **Text Sanitization** on extracted text + add a **Redaction Layer** to strip PII / PHI before ingestion (GDPR compliance)
- [ ] Run **PDF Loader in an isolated sandbox** (separate from the FAQ Engine) to prevent malicious document content from affecting the main pipeline
- [ ] Use peristenct Vector Store
- [ ] Add **Observability & Monitoring**

## Getting Started
 
### Prerequisites
 
- Python 3.x
- An Anthropic API key
- An OpenAI API key
 
### 1. Clone the Repository
 
```bash
git clone <repo-url>
cd <repo-name>
```
 
### 2. Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Configure Environment Variables
 
Create a `.env.local` file in the root of the project:
 
```env
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
APP_ENV=local
```
 
### 5. Create a Test File
 
Create a `test.py` file in the root of the project:
 
```python
from app import generate_faqs

if __name__ == "__main__":
    audience = ["audience 1", ...]

    path = "./path-to-file"

    result = generate_faqs(audience, path=path)

    with(open("generated_faqs.md", "w") as faq_file):
        faq_file.write(result)

    print("Generated FAQs in markdown format:", result)
```
 
> `audience_section` is a list of audience types relevant to the document.
> For example, for an IELTS document: `["test_takers", "test_centers"]`
 
### 6. Add Test File to Launch Config
 
In `.vscode/launch.json`, add an entry for `test.py`:
 
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run FAQ Engine",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/faqtory-app/test.py",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/faqtory-app/.env.local",
            "env": {
                "APP_ENV": "local"
            }
        }
    ]
}
```
 
> The `envFile` field ensures `pydantic_settings` picks up your API keys and `APP_ENV` from `.env.local`
 
### 7. Run via VS Code
 
Open the **Run & Debug** panel (`Ctrl+Shift+D` / `Cmd+Shift+D`), select **Run FAQ Engine** and click ▶️
 
### 8. View Generated FAQs
 
The generated FAQs will be saved to `generated_faqs.md` in the root of the project.
 
---
 