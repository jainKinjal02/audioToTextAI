import os
from pydub import AudioSegment

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

# Example usage
if __name__ == "__main__":
    # Replace with your input WAV file path
    input_file = "/Users/kinjal/Desktop/MyProjects/audioToText/output.wav"
    
    # Optional: specify a custom output directory
    output_dir = "/Users/kinjal/Desktop/MyProjects/audioToText/wavchunks"
    
    # Split the file
    chunk_files = split_wav_into_chunks(input_file)
    
    print("Audio file split into the following chunks:")
    for file in chunk_files:
        print(file)