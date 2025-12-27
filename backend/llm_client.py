import os
#import openai
from pydantic import BaseModel
import json
from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        OpenAI.api_key = self.api_key
        self.client = OpenAI(api_key=self.api_key)



    def call_llm(self, messages: list, tools: list = None):
        # Executes a streaming LLM call using the OpenAI Responses API.
        
        response = self.client.responses.create(
            model="gpt-5",
            input=messages,
            tools=tools,
            stream=True
        )
        

        full_text = ""
        tool_calls = []

        current_tool = None
        current_args = ""


        for event in response:
            
            # 🔹 Stream text if available
            if event.type == "response.output_text.delta" and hasattr(event, "delta"):
                print(event.delta, end="", flush=True)
                full_text += event.delta

            # 🔹 New function call detected
            elif event.type == "response.output_item.added" and hasattr(event, "item"):
                item = event.item
                if getattr(item, "type", "") == "function_call":
                    current_tool = {
                        "id": getattr(item, "id", None),
                        "name": getattr(item, "name", None),
                        "arguments": None
                    }
                    current_args = ""

            # 🔹 Arguments delta streamed
            elif event.type == "response.function_call_arguments.delta" and hasattr(event, "delta"):
                current_args += event.delta

            # 🔹 Arguments complete → finalize tool call
            elif event.type == "response.function_call_arguments.done":
                if current_tool is not None:
                    current_tool["arguments"] = current_args
                    tool_calls.append(current_tool)
                    #print("Tool call completed:", current_tool)
                    current_tool = None
                    current_args = ""

            # 🔹 Response completed
            elif event.type == "response.completed":
                print("\n[Response completed]")

        print("All tool calls collected:" , tool_calls)
        
        
        return {
            "content": full_text,
            "tool_calls": tool_calls
        }


