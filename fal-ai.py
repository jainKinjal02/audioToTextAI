import fal_client
import os

# Set your API key directly in the code (ensure this is secure)
fal_client.api_key = os.getenv("FAL_KEY")  # Ensure FAL_KEY is set in your environment

def on_queue_update(update):
    """Callback function to handle queue updates."""
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

# Specify the audio file path and language
audio_file_path = "https://drive.google.com/drive/folders/1oQfPz7jTlz_gXyFAIVFP0vnNZai9BNWP"

# Check if the audio file exists
if not os.path.exists(audio_file_path):
    print(f"Error: The audio file does not exist at the specified path: {audio_file_path}")
else:
    print(f"Audio file found: {audio_file_path}")  # Debugging line
    # Subscribe to the whisper model for speech-to-text conversion
    try:
        result = fal_client.subscribe(
            "fal-ai/whisper",
            arguments={
                "audio_url": audio_file_path,  # Ensure this is a valid URL or accessible path
                "language": "hi"  # Specify Hindi language
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        # Print the result of the subscription
        print(result)
    except Exception as e:
        print(f"An error occurred during subscription: {str(e)}")