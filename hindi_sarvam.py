import os
from pydub import AudioSegment
import requests
import logging
from openai import OpenAI

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key="")  # Add your OpenAI API key here

def split_wav_into_chunks(input_file, chunk_length_ms=60000, output_dir=None):
    """
    Split a WAV file into chunks of specified length (default 1 minute).
    
    :param input_file: Path to the input WAV file
    :param chunk_length_ms: Length of each chunk in milliseconds (default 60000 = 1 minute)
    :param output_dir: Directory to save chunks (if None, uses input file's directory)
    :return: List of paths to created chunk files
    """
    # Load the audio file
    audio = AudioSegment.from_wav(input_file)
    
    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the base filename without extension
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    
    # List to store chunk file paths
    chunk_files = []
    
    # Split the audio into chunks
    for i, chunk_start in enumerate(range(0, len(audio), chunk_length_ms)):
        # Extract the chunk
        chunk = audio[chunk_start:chunk_start + chunk_length_ms]
        
        # Create output filename
        chunk_filename = os.path.join(
            output_dir, 
            f"{base_filename}_chunk_{i+1}.wav"
        )
        
        # Export the chunk
        chunk.export(chunk_filename, format="wav")
        chunk_files.append(chunk_filename)
    
    return chunk_files

def convert_audio_to_text(audio_file):
    url = "https://api.sarvam.ai/speech-to-text"
    payload = {
        'model': 'saarika:v1',
        'language_code': 'hi-IN',
        'with_timestamps': 'false'
    }
    files = [
        ('file', (os.path.basename(audio_file), open(audio_file, 'rb'), 'audio/wav'))
    ]
    headers = {
        'api-subscription-key': ''
    }

    response = requests.post(url, headers=headers, data=payload, files=files)
    return response.text

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
    # Replace with your input WAV file path
    input_file = "/Users/kinjal/Desktop/MyProjects/audioToText/audio/hindi.wav"
    
    # Optional: specify a custom output directory
    output_dir = "/Users/kinjal/Desktop/MyProjects/audioToText/"
    
    # Split the file
    chunk_files = split_wav_into_chunks(input_file, output_dir=output_dir)
    
    print("Audio file split into the following chunks:")
    
    # Initialize a variable to hold the full transcription
    full_transcription = ""
    
    for file in chunk_files:
        print(file)
        # Convert each chunk to text
        text_response = convert_audio_to_text(file)
        
        # Append the transcribed text to the full transcription
        full_transcription += text_response + "\n"  # Add a newline for separation
    
    # Improve the combined transcribed text
    improved_text = improve_text(full_transcription)
    
    # Save the improved text to a single file
    output_file_path = os.path.join(output_dir, "improved_transcription.txt")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(improved_text)
    
    print(f"Improved transcription saved to {output_file_path}")