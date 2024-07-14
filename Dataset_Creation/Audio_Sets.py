import os
import random
import shutil
import pandas as pd
import soundfile as sf


def get_audio_duration(file_path):
    """
    Get the duration of a WAV audio file.

    Args:
        file_path (str): Path to the WAV audio file.

    Returns:
        float: Duration of the audio file in seconds.
    """
    with sf.SoundFile(file_path) as audio_file:
        return len(audio_file) / audio_file.samplerate


def split_audio_files(original_folder, output_folder, excel_file, target_duration=1):
    """
    Splits WAV audio files with a specific duration from the original folder into three groups:
    train, validation, and test. Ensures samples from the same source file are not split across groups.

    Args:
        original_folder (str): Path to the folder containing the original audio files.
        output_folder (str): Path to the folder where the output groups will be created.
        excel_file (str): Path to the Excel file containing the metadata about the audio samples.
        target_duration (float): Target duration of the audio files in seconds. Default is 1.

    Output:
        Three folders ('train', 'validation', 'test') are created within the output_folder.
        The audio files are copied into these folders based on the specified proportions.
        A new Excel file is created with all fields from the original file plus an additional column indicating the set.

    Purpose:
        This function shuffles the WAV audio files in the original folder and then divides them
        into three groups with specified proportions for train, validation, and test.
        It ensures that each group contains a random and non-repeating selection of files
        with a specific duration.
    """
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Filter the dataframe for rows with the target duration
    df = df[df['Segment Length (s)'] == target_duration]

    # Get a list of unique source files
    source_files = df['Source File'].unique()

    # Shuffle the list of source files to ensure randomness
    random.shuffle(source_files)

    # Calculate the number of source files for each group
    total_sources = len(source_files)
    train_count = int(0.8 * total_sources)
    validation_count = test_count = int(0.1 * total_sources)

    # Create folders for each group if they don't exist
    for group in ['train', 'validation', 'test']:
        os.makedirs(os.path.join(output_folder, group), exist_ok=True)

    # Assign source files to groups
    train_sources = source_files[:train_count]
    validation_sources = source_files[train_count:train_count + validation_count]
    test_sources = source_files[train_count + validation_count:]

    # Create a dictionary to map each source file to its respective group
    source_to_group = {}
    for source in train_sources:
        source_to_group[source] = 'train'
    for source in validation_sources:
        source_to_group[source] = 'validation'
    for source in test_sources:
        source_to_group[source] = 'test'

    # Add a new column to the dataframe indicating the group for each sample
    df['Set'] = df['Source File'].map(source_to_group)

    # Save the updated dataframe to a new Excel file
    output_excel_file = os.path.join(output_folder, 'updated_segments.xlsx')
    df.to_excel(output_excel_file, index=False)

    # Helper function to copy files to the respective group folder
    def copy_files_to_group(group_name, sources):
        for source in sources:
            segment_names = df[df['Source File'] == source]['Segment Name']
            for file in segment_names:
                shutil.copy(os.path.join(original_folder, file), os.path.join(output_folder, group_name, file))

    # Copy files to their respective groups
    copy_files_to_group('train', train_sources)
    copy_files_to_group('validation', validation_sources)
    copy_files_to_group('test', test_sources)


def main():
    original_folder = 'add path to original folder here'
    output_folder = 'add path to output folder here'
    excel_file = 'add path to excel file here'
    target_duration = 3  # or any other duration you need

    split_audio_files(original_folder, output_folder, excel_file, target_duration)


if __name__ == "__main__":
    main()
