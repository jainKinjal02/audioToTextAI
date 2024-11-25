import os
import requests
import logging
from pydub import AudioSegment
from openai import OpenAI

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key="")

def split_audio(audio_path, chunk_length_ms):
    """Splits the audio file into smaller chunks."""
    audio = AudioSegment.from_file(audio_path)
    chunks = []
    
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_name = f"chunk_{i // chunk_length_ms}.mp3"
        chunk.export(chunk_name, format="mp3")
        chunks.append(chunk_name)
    
    return chunks

def transcribe_hindi_audio(audio_path):
    """Transcribes the given audio file using the OpenAI API."""
    try:
        api_key = ""  # Use an environment variable for the API key
        
        logger.info(f"Starting transcription of {audio_path}")
        with open(audio_path, 'rb') as audio_file:
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": "whisper-1",
                "language": "hi",
                "task": "transcribe"
            }
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers,
                files={"file": audio_file},
                data=data
            )
        
        if response.status_code == 200:
            result = response.json()
            return result["text"]
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")
            raise Exception("API call failed")

    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise

def improve_text(original_text):
    """Improves the generated text using the OpenAI API."""
    try:
        logger.info("Improving the generated text...")
        improvement_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in Hindi Language and Jain Scriptures. You will be provided with a hindi transcript. There are mistakes in the transcription due to limitation in hindi speech to text system. Your task is to get the correct hindi words ,keep the content and intent as it is. Do not skip any details - just correct incoherent parts of the text. Output only the final hindi text with all things said in the audio and nothing else."},
                {
                    "role": "user",
                    "content": f"{original_text}"
                }
            ]
        )
        improved_text = improvement_completion.choices[0].message.content
        return improved_text

    except Exception as e:
        logger.error(f"Error during text improvement: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    audio_file = "/Users/kinjal/Desktop/MyProjects/audioToText/मंगलाचरण .m4a"  # Update to your audio file
    output_file = "hindi_transcription_1.txt"
    chunk_length = 10 * 60 * 1000  # 3 minutes in milliseconds

    # Step 1: Split the audio
    chunks = split_audio(audio_file, chunk_length)

    # Step 2: Transcribe each chunk and collect results
    full_transcription = ""
    for chunk in chunks:
        try:
            logger.info(f"Transcribing {chunk}...")
            transcribed_text = transcribe_hindi_audio(chunk)
            full_transcription += transcribed_text + "\n"  # Combine results
            
            # Step 3: Improve the generated transcription
            improved_text = improve_text(transcribed_text)
            full_transcription += f"Improved: {improved_text}\n"  # Append improved text

        except Exception as e:
            logger.error(f"An error occurred while processing {chunk}: {str(e)}")

    # Step 4: Save the full transcription to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_transcription)

    logger.info(f"Full transcription saved to {output_file}")