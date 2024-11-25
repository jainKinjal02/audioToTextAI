import requests
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe_hindi_audio(audio_path, output_path):
    try:
        # Perform transcription using API with large model
        api_key = os.getenv("OPENAI_API_KEY") ;
        logger.info(f"Starting transcription of {audio_path}")
        with open(audio_path, 'rb') as audio_file:
            headers = {
                 "Authorization": f"Bearer {api_key}" # Replace with your actual API key
            }
            data = {
                "model": "whisper-1",  # Use the correct transcription model
                "language": "hi",      # Hindi language
                "task": "transcribe"   # Transcription task
            }
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",  # Replace with actual API endpoint
                headers=headers,  # Include the headers with the API key
                files={"file": audio_file},
                data=data  # Specify large model
            )
        
        if response.status_code == 200:
            result = response.json()
            # Save transcription to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result["text"])
            logger.info(f"Transcription saved to {output_path}")
            return result["text"]
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")
            raise Exception("API call failed")

    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    # Replace these paths with your actual audio file path
    audio_file = "/Users/kinjal/Desktop/MyProjects/audioToText/don_dialogue.mp3"
    output_file = "hindi_transcription.txt"
    
    try:
        transcribed_text = transcribe_hindi_audio(audio_file, output_file)
        print("\nFirst 200 characters of transcription:")
        print(transcribed_text[:200])
    except Exception as e:
        print(f"An error occurred: {str(e)}")