#from llm_client import LLMClient

from backend.llm_client import LLMClient
from backend.tools import ToolExecutor

import json



# Define tools for OpenAI
# Define tools for OpenAI Responses API
TOOLS = [
    {
        "type": "function",
        "name": "get_medication_by_name",
        "description": "Retrieve factual medication info",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the medication"
                }
            },
            "required": ["name"]
        }
    },
    {
        "type": "function",
        "name": "check_stock",
        "description": "Check stock availability of medication",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the medication"
                }
            },
            "required": ["name"]
        }
    },
    {
        "type": "function",
        "name": "check_prescription_requirement",
        "description": "Check if a prescription is required for a medication",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the medication"
                }
            },
            "required": ["name"]
        }
    },
    {
        "type": "function",
        "name": "get_active_ingredients",
        "description": "Get active ingredients of a medication",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the medication"
                }
            },
            "required": ["name"]
        }
    },
    {
        "type": "function",
        "name": "get_dosage_info",
        "description": "Return dosage and usage instructions for a medication",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the medication"
                }
            },
            "required": ["name"]
        }
    },
    {
        "type": "function",
        "name": "get_user_by_name",
        "description": "Retrieve basic information about a user",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Full name of the user"}
            },
            "required": ["name"]
        }
    },
    {
        "type": "function",
        "name": "list_users",
        "description": "Return a list of all synthetic users (for testing or conversation)",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "get_user_medications",
        "description": "Return the medications assigned to a specific user",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Full name of the user"}
            },
            "required": ["name"]
        }
    }
]



def run_agent_step_stream(user_input, messages, llm=None, tools=None, max_iterations=5):
    
    """
    Streams the AI agent's response to user input, executing any tools 
    as needed and yielding incremental updates including tool results and the final response.
    """
    
    if llm is None:
        llm = LLMClient()
    if tools is None:
        tools = ToolExecutor()

    messages.append({"role": "user", "content": user_input})
    yield "Agent is thinking...\n"
    
    collected_tool_results = {}
    print("Called LLM")
    llm_response = llm.call_llm(messages, tools=TOOLS)

    if llm_response.get("tool_calls"):
        for call in llm_response["tool_calls"]:
            
            
            tool_name = call["name"]
            args = json.loads(call["arguments"]) if call["arguments"] else {}
            med_name = args.get("name")
            print("DEBUG tool_name:", tool_name)
            print("\nDEBUG call:", call)


            yield f"→ Calling tool: {tool_name}\n"

            if tool_name == "get_medication_by_name":
                result = tools.get_medication_by_name(med_name)

            elif tool_name == "check_stock":
                result = tools.check_stock(med_name)

            elif tool_name == "check_prescription_requirement":
                result = tools.check_prescription_requirement(med_name)

            elif tool_name == "get_active_ingredients":
                result = tools.get_active_ingredients(med_name)

            elif tool_name == "get_dosage_info":
                result = tools.get_dosage_info(med_name)

            elif tool_name == "get_user_by_name":
                result = tools.get_user_by_name(args.get("name"))

            elif tool_name == "list_users":
                result = tools.list_users()

            elif tool_name == "get_user_medications":
                print("Called get user medic!!!")
                result = tools.get_user_medications(args.get("name"))

            else:
                #result = {"error": "Unknown tool"}
                result = {
                    "message": "Hmm, I’m not sure about that. Can I help you with a medication or something in our pharmacy?"
                }

            collected_tool_results[tool_name] = result
            yield f"✓ Tool result: {result}\n"

            messages.append({
                "role": "assistant",
                "content": f"[Tool output: {tool_name}] {json.dumps(result)}"
            })

    final_prompt = messages + [
        {
            "role": "user",
            "content": f"Use this data if present: {json.dumps(collected_tool_results)}"
        }
    ]

    final_answer = llm.call_llm(final_prompt, tools=None)["content"]
    messages.append({"role": "assistant", "content": final_answer})

    yield f"\nAgent: {final_answer}\n"

