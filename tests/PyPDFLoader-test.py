from langchain_community.document_loaders import PyPDFLoader

path = "../data/Understanding_Climate_Change.pdf"

loader = PyPDFLoader(path)
pages = loader.load()

print(pages[0].page_content)
print(pages[0].metadata)
