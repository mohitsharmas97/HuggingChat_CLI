from transformers import pipeline

def load_model():
    """
    Loads the 'google/flan-t5-small' model, which is good
    at following instructions and answering questions.
    """
    model_name = "google/flan-t5-small"
    print(f"Loading model '{model_name}'...")
    try:
        # Use "text2text-generation" pipeline for instruction-following models
        chatbot_pipeline = pipeline("text2text-generation", model=model_name)
        print("Model loaded successfully.")
        return chatbot_pipeline
    except Exception as e:
        print(f"Error loading model: {e}")
        return None