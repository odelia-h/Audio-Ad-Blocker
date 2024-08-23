from pydub import AudioSegment
import os


def cut_audio_segment(file_path, start_minute, start_second, end_minute, end_second, output_path):
    """
    Cuts a segment from a WAV audio file and saves it to a specified location.

    Parameters:
    file_path (str): Path to the input WAV file.
    start_minute (int): Start minute of the segment.
    start_second (int): Start second of the segment.
    end_minute (int): End minute of the segment.
    end_second (int): End second of the segment.
    output_path (str): Path where the output WAV file will be saved.

    Returns:
    None
    """
    # Load the audio file
    audio = AudioSegment.from_wav(file_path)

    # Convert start and end times to milliseconds
    start_time = (start_minute * 60 + start_second) * 1000
    end_time = (end_minute * 60 + end_second) * 1000

    # Cut the audio segment
    audio_segment = audio[start_time:end_time]

    # Export the cut segment to a new file
    audio_segment.export(output_path, format="wav")

    print(f"Segment saved to {output_path}")


def main():
    # Example usage
    input_file = "add path here"

    # Output file will be saved in the current project folder
    output_file = "add path here"

    # Define the start and end times
    start_minute, start_second = 2, 0
    end_minute, end_second = 8, 0

    # Call the function to cut the audio segment
    cut_audio_segment(input_file, start_minute, start_second, end_minute, end_second, output_file)


if __name__ == "__main__":
    main()
