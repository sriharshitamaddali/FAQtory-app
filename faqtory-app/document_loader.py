from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader

#### Reads data from a PDF file or folder -- should accept path to a PDF file or a folder containing PDF files. The loader will extract text content from the PDFs and return it in a structured format, along with metadata such as file name and page number.

class PDFDocumentLoader:
    def __init__(self, file_path: str):
        self.loader = OpenDataLoaderPDFLoader(
            file_path=file_path,
            format="text",
            split_pages=True,
            use_struct_tree=True,
            keep_line_breaks=True,
            image_output="embedded",
            reading_order="xycut",
        )


    def extract_text_from_file(self) -> list[dict]:
        # Use OpenDataLoaderPDFLoader to extract text content from the PDF file
        #image_output -- keep it default embedded
        documents = self.loader.load()
        return documents