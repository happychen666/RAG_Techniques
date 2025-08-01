from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from pathlib import Path

class CustomPDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        # 获取真实 PDF 元信息
        reader = PdfReader(self.file_path)
        pdf_metadata = reader.metadata or {}
        metadata_common = {
            "title": pdf_metadata.get("/Title", ""),
            "author": pdf_metadata.get("/Author", ""),
            "creator": pdf_metadata.get("/Creator", ""),
            "producer": pdf_metadata.get("/Producer", ""),
            "creation_date": pdf_metadata.get("/CreationDate", ""),
            "mod_date": pdf_metadata.get("/ModDate", ""),
            "source": str(Path(self.file_path).resolve())
        }

        # 用 PyPDFLoader 加载文本
        text_loader = PyPDFLoader(self.file_path)
        pages = text_loader.load()

        # 给每一页补充真实元数据
        documents = []
        for i, page in enumerate(pages):
            enriched_metadata = dict(metadata_common)  # 复制一份公共 metadata
            enriched_metadata["page"] = page.metadata.get("page", i)
            enriched_metadata["keyword"] = '这里假装通过LLM提取或者NER提取'
            documents.append(Document(
                page_content=page.page_content,
                metadata=enriched_metadata
            ))

        return documents


path = "../data/Understanding_Climate_Change.pdf"
loader = CustomPDFLoader(path)
docs = loader.load()

# 打印第1页的内容和元信息
print("内容:\n", docs[0].page_content[:300])  # 只打印前300个字符
print("\n元信息:\n", docs[0].metadata)
