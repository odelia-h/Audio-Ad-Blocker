# Import relevant libraries for working with audio files as well as audio
# embedding
import librosa
import openl3
import numpy as np
from pydub import AudioSegment
import io


def extract_audio_embedding(audio_data, sample_rate):
    """
    Extract audio embeddings using OpenL3.

    Parameters:
    - audio_data: The audio signal.
    - sample_rate: The sample rate of the audio signal.

    Returns:
    - flat_embedding: The flattened audio embedding.
    """

    # Set the desired embedding size
    embedding_size = 512

    try:
        # Extract embeddings using OpenL3
        embedding, _ = openl3.get_audio_embedding(audio_data, sample_rate,
                                                  content_type="music",
                                                  embedding_size=embedding_size)

        # Flatten the embedding
        flat_embedding = np.ravel(embedding)

        return flat_embedding

    except Exception as e:
        # Handle any errors that might occur during the embedding
        # extraction process
        print("Error occurred during audio embedding extraction:", e)
        return None


def load_audio(file_path):
    """
    Load an audio file and return the audio data and sample rate.

    Parameters:
    - file_path: The path to the audio file.

    Returns:
    - audio_data: The audio signal.
    - sample_rate: The sample rate of the audio file.
    """
    try:
        # Load the audio file using librosa
        audio_data, sample_rate = librosa.load(file_path, sr=None)

        return audio_data, sample_rate
    except Exception as e:
        # Handle any errors that might occur during the loading process
        print("Error occurred during audio loading:", e)
        return None, None


def convert_audio_to_embedding(audio_segment):
    """
    Convert an AudioSegment to an audio embedding using OpenL3.

    Parameters:
    - audio_segment: The AudioSegment object containing audio data.

    Returns:
    - embedding: The audio embedding.
    """
    try:
        # Convert AudioSegment to bytes
        audio_bytes = io.BytesIO()
        audio_segment.export(audio_bytes, format='wav')
        audio_bytes.seek(0)

        # Load audio bytes with librosa
        audio_data, sample_rate = librosa.load(audio_bytes, sr=None)

        # Extract audio embedding
        embedding = extract_audio_embedding(audio_data, sample_rate)

        return embedding

    except Exception as e:
        print("Error occurred during audio to embedding conversion:", e)
        return None


# Example usage:
# Assuming you have an AudioSegment object named 'audio_segment'
audio_segment = AudioSegment.from_file("/content/drive/MyDrive/AD-Blocker Project/DEMO files/first_pod_segment.wav")

embedding = convert_audio_to_embedding(audio_segment)
if embedding is not None:
    print("Successfully converted audio to embedding.")
else:
    print("Conversion to embedding failed.")





































# # Import relevant libraries for working with audio files as well as audio
# # embedding
# import librosa
# import openl3
# import numpy as np
#
#
# def extract_audio_embedding(audio_data, sample_rate):
#     """
#     Extract audio embeddings using OpenL3.
#
#     Parameters:
#     - audio_data: The audio signal.
#     - sample_rate: The sample rate of the audio signal.
#
#     Returns:
#     - flat_embedding: The flattened audio embedding.
#     """
#
#     # Set the desired embedding size
#     embedding_size = 512
#
#     try:
#         # Extract embeddings using OpenL3
#         embedding, _ = openl3.get_audio_embedding(audio_data, sample_rate,
#                                                   content_type="music",
#                                                   embedding_size=embedding_size)
#
#         # Flatten the embedding
#         flat_embedding = np.ravel(embedding)
#
#         return flat_embedding
#
#     except Exception as e:
#         # Handle any errors that might occur during the embedding
#         # extraction process
#         print("Error occurred during audio embedding extraction:", e)
#         return None
#
#
# def load_audio(file_path):
#     """
#     Load an audio file and return the audio data and sample rate.
#
#     Parameters:
#     - file_path: The path to the audio file.
#
#     Returns:
#     - audio_data: The audio signal.
#     - sample_rate: The sample rate of the audio file.
#     """
#     try:
#         # Load the audio file using librosa
#         audio_data, sample_rate = librosa.load(file_path, sr=None)
#
#         return audio_data, sample_rate
#     except Exception as e:
#         # Handle any errors that might occur during the loading process
#         print("Error occurred during audio loading:", e)
#         return None, None
#
#
# def convert_file_to_embedding(file_name, file_path):
#
#   if file_name.endswith('.wav'):  # Process only WAV audio files
#       duration = librosa.get_duration(filename=file_path)
#       if duration < 5.0:  # Check duration
#           return 0
#       audio_data, sample_rate = load_audio(file_path)  # Define load_audio function
#       embedding = extract_audio_embedding(audio_data, sample_rate)  # Define extract_audio_embedding function
#
#
#   return embedding
#
#
# # first_pod_demo_embedding = convert_file_to_embedding("first_pod_segment.wav","/content/drive/MyDrive/AD-Blocker Project/DEMO files/first_pod_segment.wav")