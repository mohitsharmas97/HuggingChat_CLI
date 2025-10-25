
class ChatMemory:
    """
    Manages conversation history for an instruction-following model.
    It builds a prompt telling the model to answer a question
    based on the previous context.
    """
    def __init__(self, max_turns=5):
        """
        Initializes the memory.
        :param max_turns: The number of user/bot turn *pairs* to remember.
        """
        self.history = []
        # max_turns=3 means 3 user inputs and 3 bot responses
        self.max_turns = max_turns

    def add_message(self, role, content):
        """
        Adds a new message (from 'User' or 'Bot') to the history.
        """
        self.history.append({"role": role, "content": content})
        self.trim_history()

    def trim_history(self):
        """
        Applies the sliding window[cite: 14].
        If history exceeds max_turns * 2 (user + bot),
        it removes the oldest turn (2 messages).
        """
        max_messages = self.max_turns * 2
        if len(self.history) > max_messages:
            # Remove the oldest turn (one user input, one bot response)
            self.history = self.history[-max_messages:]

    def get_formatted_prompt(self):
        """
        Formats the chat history into a single string instruction
        for the text2text-generation model.
        """
        if not self.history:
            return "" 

        # Get the last user input (the current question)
        current_question = self.history[-1]['content']

        # Get the rest of the history as context
        context = ""
        for msg in self.history[:-1]: # All messages *before* the current one
            context += f"{msg['role']}: {msg['content']}\n"

        # Create a clear instruction-based prompt
        if not context:
            # This is the first turn
            prompt = f"Answer the following question: {current_question}"
        else:
            # This is a follow-up turn, so we provide context
            prompt = (f"This is the conversation history:\n{context}\n"
                      f"Based on this history, answer the new question: {current_question}")
        
        return prompt