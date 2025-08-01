# from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
from deepeval.models.base_model import DeepEvalBaseLLM

class CustomOpenAI(DeepEvalBaseLLM):
    def __init__(
        self,
        model
    ):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return "Custom OpenAI Model"

# Replace these with real values
custom_model = ChatOpenAI(
    model="gpt-4o",  # or "gpt-4-vision-preview"
    openai_api_base=os.getenv("openai_api_base"),
    openai_api_key=os.getenv("openai_api_key")
)
openai = CustomOpenAI(model=custom_model)
print(openai.generate("Write me a joke"))