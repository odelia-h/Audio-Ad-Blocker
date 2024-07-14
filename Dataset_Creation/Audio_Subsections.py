import os
import soundfile as sf
import pandas as pd
import time

def load_audio(audio_file_path):
    """
    Load audio from the specified file path using soundfile library.

    Args:
    - audio_file_path (str): Path to the audio file.

    Returns:
    - np.ndarray: Loaded audio data.
    - int: Sample rate of the audio data.
    """
    audio, sample_rate = sf.read(audio_file_path)
    return audio, sample_rate

def create_output_folder(output_folder):
    """
    Create the output folder if it doesn't exist.

    Args:
    - output_folder (str): Path to the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def split_audio(audio, sample_rate, segment_duration):
    """
    Split the audio into segments of specified duration.

    Args:
    - audio (np.ndarray): Audio data.
    - sample_rate (int): Sample rate of the audio data.
    - segment_duration (float): Duration of each segment in seconds.

    Returns:
    - list: List of audio segments.
    """
    num_samples_per_segment = int(sample_rate * segment_duration)

    num_segments = len(audio) // num_samples_per_segment
    remainder_samples = len(audio) % num_samples_per_segment

    audio_segments = []

    for i in range(num_segments):
        start_sample = i * num_samples_per_segment
        end_sample = start_sample + int(sample_rate * segment_duration)  # Dynamically calculate end_sample
        segment = audio[start_sample:end_sample]
        audio_segments.append(segment)

    # Handle the remaining samples
    if remainder_samples > 0:
        segment = audio[num_segments * num_samples_per_segment:]
        audio_segments.append(segment)

    return audio_segments


def save_audio_segments(audio_segments_info, output_folder):
    """
    Save audio segments information to an Excel file.

    Args:
    - audio_segments_info (list): List of dictionaries containing segment information.
    - output_folder (str): Path to the output folder.
    """
    excel_file_path = os.path.join(output_folder, 'audio_segments.xlsx')
    df = pd.DataFrame(audio_segments_info)
    df.to_excel(excel_file_path, index=False)
    print(f"Excel file saved as {excel_file_path}")


def process_audio(audio_file_paths, output_folder, segment_duration):
    """
    Process multiple audio files by splitting them into segments and saving segment information.

    Args:
    - audio_file_paths (list): List of audio file paths.
    - output_folder (str): Path to the output folder.
    - segment_duration (float): Duration of each segment in seconds.
    """
    all_segments_info = []

    for audio_file_path in audio_file_paths:
        print(f"Processing audio file: {audio_file_path}")
        audio, sample_rate = load_audio(audio_file_path)
        source_file_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        audio_segments = split_audio(audio, sample_rate, segment_duration)

        for i, segment in enumerate(audio_segments):
            segment_name = f"{source_file_name}_segment_{i + 1}.wav"
            segment_path = os.path.join(output_folder, segment_name)
            sf.write(segment_path, segment, sample_rate)

            start_time = i * segment_duration
            end_time = start_time + len(segment) / sample_rate
            segment_length = end_time - start_time

            all_segments_info.append({
                'Segment Name': segment_name,
                'Source File': source_file_name,
                'Start Time (s)': start_time,
                'End Time (s)': end_time,
                'Segment Length (s)': segment_length
            })

    print("Creating output folder...")
    create_output_folder(output_folder)

    print("Saving audio segments information...")
    save_audio_segments(all_segments_info, output_folder)

    print("Audio processing completed.")


def main():
    start_time = time.time()

    segment_duration = 3  # Duration of each segment in seconds
    audio_folder = "add audio_folder path here"
    output_folder = "add output_folder path here"

    audio_file_paths = [os.path.join(audio_folder, file) for file in os.listdir(audio_folder) if file.endswith('.mp3') or file.endswith('.wav')]
    print("Audio files to process:")
    print(audio_file_paths)
    process_audio(audio_file_paths, output_folder, segment_duration)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


if __name__ == "__main__":
    main()
