import whisper
import torch

def transcribe_to_hindi(audio_path):
    # Load the Whisper model (using medium model for better accuracy)
    model = whisper.load_model("medium")
    
    # Transcribe the audio file
    # Setting language to Hindi and task to transcribe
    result = model.transcribe(
        audio_path,
        language="hi",
        task="transcribe",
        fp16=torch.cuda.is_available()  # Use GPU if available
    )
    
    # Return the transcribed text
    return result["text"]

if __name__ == "__main__":
    # Example usage
    audio_file = "path/to/your/audio.mp3"  # Support formats: mp3, wav, m4a, etc.
    hindi_text = transcribe_to_hindi(audio_file)
    
    # Save the transcription to a file
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(hindi_text)