# interface.py
import model_loader
import chat_memory

def main():
    """
    Main CLI loop for the chatbot.
    """
    # 1. Load Model
    chatbot = model_loader.load_model()
    if chatbot is None:
        print("Failed to load model. Exiting.")
        return

    # 2. Initialize Memory
    memory = chat_memory.ChatMemory(max_turns=5) 
    
    print("\n--- Local Chatbot Initialized (using flan-t5-small) ---")
    print("Type your message and press Enter. Type '/exit' to quit.")

    # 3. Start CLI loop
    while True:
        try:
            # 3a. Accept user input
            user_input = input("User: ")

            # 3b. Check for exit command
            if user_input.strip().lower() == '/exit':
                print("Bot: Exiting chatbot. Goodbye!")
                break
            
            # 3c. Add user input to memory
            memory.add_message("User", user_input)
            
            # 3d. Get the full conversation context as a single string
            prompt = memory.get_formatted_prompt()

            # 3e. Get model response
            # The pipeline returns a list of dictionaries
            response_list = chatbot(prompt, max_length=100, num_return_sequences=1)
            bot_response = response_list[0]['generated_text'].strip()

            # 3f. Print the bot response
            print(f"Bot: {bot_response}")

            # 3g. Add bot's response to memory
            memory.add_message("Bot", bot_response)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nBot: Exiting chatbot. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()