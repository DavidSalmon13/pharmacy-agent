import tkinter as tk
import threading
from backend.main import run_agent_step_stream  # <-- streaming version


SYSTEM_PROMPT =  """
    You are an AI-powered pharmacy assistant for a retail pharmacy chain. Your purpose is to assist customers with factual information about medications and related pharmacy operations using the tools provided. 

POLICIES:
- ALWAYS provide factual information only.
- If asked for an item, always check if present in stock (even if is not medication), if quantity is 0, we don't sell the item.
- NEVER give medical advice, make diagnoses, or recommend purchases. 
- If a user requests medical advice or health guidance, politely redirect them to a licensed healthcare professional. 
- Respond in the language used by the user (English or Hebrew). 
- Keep answers concise: one sentence for factual information unless a multi-step flow is explicitly required.
- If no information found, ask the user: "Hmm, I’m not sure about that. Can I help you with a medication or something in our pharmacy?"
- Do not include tool call details in your response text; only answer naturally based on tool outputs.

RESPONSE RULES:
- Only use information from the tools to answer questions.
- For multi-step flows, combine tool calls in logical sequences to resolve the user’s request.
- Always summarize tool data into a single, factual response.
- If a tool returns no data, respond: "Information not found."
- Clearly indicate any tool calls you make when generating the response.

MULTI-STEP FLOW EXAMPLE GUIDELINES:
- For requests like "check availability and dosage for a user’s medication", the agent should:
  1. Identify the user via get_user_by_name() or list_users().
  2. Retrieve the user's medications with get_user_medications().
  3. For each medication, call check_stock(), get_dosage_info(), and other relevant tools.
  4. Summarize the factual results into a concise response.

OBJECTIVE:
- Provide clear, accurate, and factual responses.
- Stream results incrementally when possible.
- Always follow the above policies strictly.
"""


class PharmacyChatUI:
    """Provides a simple chat interface that allows users to interact with the pharmacy AI agent using real-time streaming responses."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pharmacy Chatbot")

        # Chat display
        self.chat_box = tk.Text(self.root, state=tk.DISABLED, width=90, height=25, wrap=tk.WORD)
        self.chat_box.pack(padx=10, pady=10)

        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.entry = tk.Entry(input_frame, width=75)
        self.entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)

        # Conversation memory
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # ---------------- UI Helpers ---------------- #

    def append_text(self, text: str):
        """Safely append text to chat box"""
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, text)
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    # ---------------- Chat Logic ---------------- #

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        if user_text.lower() == "exit":
            self.root.destroy()
            return

        self.entry.delete(0, tk.END)

        # Show user message immediately
        self.append_text(f"\nUser: {user_text}\n\n")

        # Start streaming agent response in background
        threading.Thread(
            target=self.stream_agent_response,
            args=(user_text,),
            daemon=True
        ).start()

    def stream_agent_response(self, user_text):
        """
        Consumes the streaming generator and updates UI incrementally
        """
        for chunk in run_agent_step_stream(user_text, self.messages):
            # Tkinter-safe UI update
            self.root.after(0, self.append_text, chunk)

    # ---------------- Run ---------------- #

    def run(self):
        self.root.mainloop()


# -------- Entry Point -------- #

if __name__ == "__main__":
    app = PharmacyChatUI()
    app.run()
