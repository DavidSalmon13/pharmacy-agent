# Pharmacy Agent

This project implements a real-time conversational AI pharmacy assistant using the OpenAI API.  
The agent assists customers through chat by answering factual questions about medications, stock availability, prescription requirements, and usage information.  

The agent is tool-driven, stateless, and supports multi-step workflows where it reasons over user input, calls backend tools, and then produces a final user-facing response.  

**Constraints:**  
- Provides factual information only  
- Does not give medical advice or diagnoses  
- Redirects advice-seeking users to healthcare professionals  
- Avoids encouraging purchases  
- Supports both English and Hebrew  

These constraints are enforced through prompt design and tool-only data usage.

---

## Prerequisites

- Python 3.12 or higher installed  
- OpenAI API Key (set as an environment variable)  
- Docker (optional, for containerized version)  
- Required Python packages (install via `pip install -r requirements.txt`)  
- Tkinter (used for GUI)  

---

## Tech Stack

- **Backend:** Python  
- **LLM:** OpenAI GPT-5  
- **UI:** Tkinter  
- **Agent Design:** Tool-augmented, multi-step flow  
- **Database:** In-memory synthetic data (10 users, 5 medications, and stock)  

---

## Agent Flow (How a Request Is Handled)

1. User sends a message through the UI.  
2. The agent sends the message to GPT-5 with available tool definitions.  
3. GPT-5 may request one or more tool calls.  
4. The agent executes the tools via `ToolExecutor`.  
5. Tool results are injected back into the conversation.  
6. GPT-5 produces a final, clean response for the user.  
7. All steps are streamed in real time.  

---

## Tools

### 1. `get_medication_by_name`
- **Purpose:** Retrieve basic information about a medication including its active ingredient, prescription requirement, and dosage instructions.  
- **Inputs:** `name` (string)  
- **Output (json):** `name` (string), `active_ingredient` (string), `prescription_required` (Boolean), `dosage_text` (string)  
- **Error Handling:** Returns an error message if the medication does not exist in the pharmacy.  
- **Fallback:** The agent responds politely that the medication is not sold in the pharmacy.  

### 2. `check_stock`
- **Purpose:** Check whether a medication is in stock and return the available quantity.  
- **Inputs:** `name` (string)  
- **Output (json):** `name` (string), `quantity` (integer), `available` (Boolean)  
- **Error Handling:** If the medication is not in stock, quantity is returned as 0 and `available` is false.  
- **Fallback:** The agent informs the user that the medication is currently unavailable.  

### 3. `check_prescription_requirement`
- **Purpose:** Determine if a medication requires a prescription.  
- **Inputs:** `name` (string)  
- **Output (json):** `name` (string), `required` (Boolean)  
- **Error Handling:** Returns a message if the medication is not found.  
- **Fallback:** The agent informs the user that the medication is not available.  

### 4. `get_active_ingredients`
- **Purpose:** Retrieve the active ingredient(s) of a medication.  
- **Inputs:** `name` (string)  
- **Output (json):** `name` (string), `active_ingredient` (string)  
- **Error Handling:** Returns an error if the medication does not exist.  
- **Fallback:** The agent indicates that the medication was not found in the pharmacy.  

### 5. `get_dosage_info`
- **Purpose:** Provide recommended dosage instructions for a medication.  
- **Inputs:** `name` (string)  
- **Output (json):** `name` (string), `dosage_text` (string)  
- **Error Handling:** Returns an error if the medication is not in the database.  
- **Fallback:** The agent informs the user that dosage information is unavailable.  

### 6. `get_user_by_name`
- **Purpose:** Retrieve basic information about a user, including email, age, and medications.  
- **Inputs:** `name` (string)  
- **Output (json):** `name` (string), `email` (string), `age` (integer), `medications` (list of strings)  
- **Error Handling:** Returns an error if the user is not found.  
- **Fallback:** The agent informs the user that the requested user does not exist.  

### 7. `list_users`
- **Purpose:** List all active users in the system.  
- **Inputs:** None  
- **Output (json):** list of objects `{name: (string), email: (string)}`  
- **Error Handling:** N/A  
- **Fallback:** N/A  

### 8. `get_user_medications`
- **Purpose:** Retrieve the medications associated with a specific user.  
- **Inputs:** `name` (string)  
- **Output (json):** `name` (string), `medications` (list of strings)  
- **Error Handling:** Returns an error if the user does not exist.  
- **Fallback:** The agent informs the user that the medications for the requested user are unavailable.  

---

## How to Run Locally

1. Ensure Python 3.12 is installed.  
2. Project structure:  
   - `backend/` ? agent logic  
   - `UI/` ? chat interface  
3. Navigate to the `UI` folder.  
4. Run the chat interface module using Python.  
5. Ensure your OpenAI API key is set as an environment variable.  
6. The GUI window will launch, allowing real-time interaction with the AI agent.  
7. Test all multi-step flows and tools, such as checking medication details or inventory status.  

---

## How to Build Docker

The project is containerized with Docker.  

1. Navigate to the root of the project (where the `Dockerfile` is located).  
2. Build the Docker image:  
   ```bash
   docker build -t pharmacy-agent .
3. The Dockerfile sets up a Python 3.12 environment, installs dependencies, and copies the project into the container.
4. Run the container, passing your OpenAI API key as an environment variable.
5. The chat interface will launch automatically, allowing testing of all tools and multi-step flows.

## Multi-Step Flows Evaluation

### Example 1

**User request:**  
> �Is ibuprofen in stock and how should it be taken?�  

**Agent flow:**  
1. The agent receives the user message.  
2. The agent calls `check_stock` to determine if ibuprofen is available.  
3. Once confirmed, the agent calls `get_dosage_info` to retrieve the recommended usage instructions.  
4. The agent combines the results from both tool calls to generate a clear, factual response.  

**Final Agent Response:**  
> �Yes, ibuprofen is in stock (8 units), and the labeled directions are: take 1 pill every 8 hours.�  

**Evaluation for Example 1:**  
- **Correct Tool Sequence:** `check_stock` ? `get_dosage_info`  
- **Accurate Response:** Stock and dosage match the database  
- **Policy Compliance:** Provides factual information only, no medical advice  
- **Clarity:** Response is concise and clear  

---

### Example 2

**User request:**  
> �What medication does Hannah Wilson use?�  

**Agent flow:**  
1. The agent receives the user message.  
2. The agent calls `get_user_by_name` to retrieve the user�s information and associated medications.  
3. The agent responds with the medication the user takes (metformin in this case).  

**Agent Response:**  
> �Hannah Wilson uses metformin�  

**Follow-up user request:**  
> �Does metformin require a prescription? How do you use it?�  

**Agent flow:**  
1. The agent calls `check_prescription_requirement` to determine if metformin requires a prescription.  
2. The agent calls `get_dosage_info` to get the recommended dosage instructions.  
3. The agent combines the results from both tools to generate a clear, factual response.  

**Final Agent Response:**  
> �Yes�metformin requires a prescription, and the dosing info on file is: take 1 pill with meals.�  

**Evaluation for Example 2:**  
- **Correct Tool Sequence:** First `get_user_by_name`, then `check_prescription_requirement` and `get_dosage_info` for the follow-up  
- **Accurate Response:** Correct medication, prescription status, and dosage retrieved from the database  
- **Multi-Step Handling:** Agent successfully manages follow-up without losing context  
- **Policy Compliance:** Provides only factual information; no advice or diagnosis given  
- **Clarity:** Responses are structured, readable, and informative  

---

### Evaluation Summary

The AI pharmacy agent successfully handles multi-step conversational flows by:  
- Correctly calling the necessary tools in sequence  
- Providing accurate information from the synthetic database  
- Maintaining full compliance with policy restrictions (factual data only)  
- Effectively managing follow-up questions  
- Retrieving stock, dosage, and prescription information accurately  
- Generating clear and concise responses for end-users  
- Supporting both English and Hebrew  

The evaluation of example flows, supported by screenshots, demonstrates the agent�s reliability, clarity, and capability to perform multi-step interactions.
