from langchain_core.callbacks import BaseCallbackHandler
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()


class EngineeringCallbackHandler(BaseCallbackHandler):

    def on_llm_start(self, serialized, prompts, **kwargs):
        print("\n[CALLBACK] LLM started")

    def on_llm_end(self, response, **kwargs):
        print("[CALLBACK] LLM completed")

    def on_llm_error(self, error, **kwargs):
        print(f"[CALLBACK] LLM error: {error}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        print(
            f"\n[CALLBACK] Tool started: "
            f"{serialized.get('name', 'unknown')}"
        )
        print(f"[CALLBACK] Tool input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"[CALLBACK] Tool completed")
        print(f"[CALLBACK] Tool output: {output}")


model = ChatGroq(
    model=os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    ),
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


if __name__ == "__main__":

    callback_handler = EngineeringCallbackHandler()

    response = model.invoke(
        "Explain HTTP 401 errors in one sentence.",
        config={
            "callbacks": [callback_handler]
        }
    )

    print("\n========== FINAL RESPONSE ==========")
    print(response.content)