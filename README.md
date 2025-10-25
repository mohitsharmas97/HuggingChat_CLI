# HuggingChat_CLI

This project is a simple, modular command-line chatbot that runs a small Hugging Face language model locally. It is designed to hold a coherent conversation by maintaining a short-term "memory" of the most recent turns.
<img width="1373" height="473" alt="image" src="https://github.com/user-attachments/assets/8fca452f-2340-4a89-9ef7-c6fb0a35e798" />


## Features

* [cite_start]**Local Model:** Runs `google/flan-t5-small` entirely on your local machine (no API keys needed)[cite: 12].
* [cite_start]**Conversational Memory:** Remembers the last 3 turns of conversation using a sliding window mechanism[cite: 14].
* [cite_start]**Modular Code:** The project is split into three clear modules[cite: 18]:
    * `model_loader.py`: Handles loading the model and tokenizer pipeline.
    * `chat_memory.py`: Manages the conversational history.
    * `interface.py`: Runs the main command-line interface (CLI) loop.
* [cite_start]**Simple CLI:** A continuous loop for chatting, with a graceful exit command (`/exit`)[cite: 16, 17].


# Setup Instructions
### 1. Prerequisites
###  Python 3.8 or newer
###   pip (Python package installer)

# Installation
### 1.Clone the repository:
    git clone <your-repo-url>
    cd <your-repo-name>
### 2.Create a virtual environment (Recommended):
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
### 3.Install the required libraries: Create a file named requirements.txt in the project's root directory:
    transformers
    torch
### Then, run the installer:
    pip install -r requirements.txt
### Once setup is complete, simply run the interface.py script:
    python interface.py

### The script will first download and cache the google/flan-t5-small model (this only happens the first time). You will then see the prompt to start chatting.
     Loading model 'google/flan-t5-small'...
     Model loaded successfully.
     --- Local Chatbot Initialized (using flan-t5-small) ---
     Type your message and press Enter. Type '/exit' to quit.
     User:

### This example shows the bot's ability to answer consecutive, related questions, just as specified in the task requirements.
    User: What is the capital of France?
    Bot: The capital of France is Paris.
    User: And what about Italy?
    Bot: The capital of Italy is Rome.
    User: /exit
    Bot: Exiting chatbot. Goodbye!
		
## Architecture & Flow

The `interface.py` script orchestrates the entire process. It loads the model once, initializes the memory, and then runs a loop that:
1.  Accepts user input.
2.  Adds the input to memory.
3.  Asks the memory module to format the *entire* context into a single prompt.
4.  Sends that prompt to the model.
5.  Prints the model's response.
6.  Adds the model's response back to memory.

This flow, especially the "sliding window" memory, allows the bot to understand follow-up questions.

```mermaid

graph TD
    Start(Start Application) --> A["Load Model via model_loader.py"];
    A --> B["Initialize ChatMemory(max_turns=5)"];
    B --> C{"Wait for User Input"};
    C --> D["Get User Input"];
    D --> E{"Input == /exit?"};
    E -- Yes --> F["Print 'Goodbye!' & Exit"];
    
    E -- No --> G["Add User Input to Memory<br>(chat_memory.add_message)"];
    G --> H["Get Formatted Prompt<br>(chat_memory.get_formatted_prompt)"];
    H --> I["Send Full Prompt to Model Pipeline"];
    I --> J["Receive Generated Response"];
    J --> K["Print Bot Response"];
    K --> L["Add Bot Response to Memory<br>(chat_memory.add_message)"];
    L --> M["Trim History if Needed<br>(chat_memory.trim_history)"];
    M --> C;
		



