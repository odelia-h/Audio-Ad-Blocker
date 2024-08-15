import math
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QDialog, QMessageBox
from pydub import AudioSegment
import joblib
import os

from Vggish_Embeddings_Model import extract_vggish_embeddings

class AudioProcessor:
    def __init__(self, svm_model_path):
        self.svm_model = joblib.load(svm_model_path)

    def convert_to_embeddings(self, file_path):
        embeddings = extract_vggish_embeddings(file_path)
        return embeddings

    def detect_ads(self, file_path):
        embedding = self.convert_to_embeddings(file_path)
        prediction = self.svm_model.predict([embedding])
        return prediction == 1

class ConfirmationDialog(QDialog):
    def __init__(self, output_path):
        super().__init__()
        self.setWindowTitle("Confirmation")

        self.label = QLabel(f"Processed audio saved successfully at: {output_path}")
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ad Detector")
        self.audio_processor = AudioProcessor('svm_model_vggish_5sec.pkl')

        self.label = QLabel("Upload an audio file (15 seconds)...")
        self.upload_button = QPushButton("Upload Audio")
        self.upload_button.clicked.connect(self.upload_audio)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def upload_audio(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "Audio Files (*.wav *.mp3);;All Files (*)", options=options)

        if file_path:
            self.close()
            self.process_audio(file_path)

    def process_audio(self, file_path):
        audio = AudioSegment.from_file(file_path)

        # Get the duration of the audio file in milliseconds
        duration_ms = len(audio)

        # Define the duration of each segment (5 seconds in milliseconds)
        segment_duration_ms = 5000

        # Calculate the number of segments
        num_segments = math.ceil(duration_ms / segment_duration_ms)

        # Create a directory to save the segments
        output_dir = "audio_segments"
        os.makedirs(output_dir, exist_ok=True)
        segments_paths=[]
        seg_list=[]
        # Loop through the audio and save each segment
        for i in range(num_segments):
            start_time = i * segment_duration_ms
            end_time = min(start_time + segment_duration_ms, duration_ms)
            segment = audio[start_time:end_time]
            seg_list.append(segment)
            segment_path = os.path.join(output_dir, f"segment_{i + 1}.wav")
            segment.export(segment_path, format="wav")
            print(f"Segment {i + 1} extracted and saved successfully as {segment_path}.")
            segments_paths.append(segment_path)

        processed_audio = AudioSegment.silent(duration=0)

        for i, seg_path in enumerate(segments_paths):
            if self.audio_processor.detect_ads(seg_path):
                pass
            #processed_audio += AudioSegment.silent(duration=len(seg_list[i]))
            else:
                processed_audio += seg_list[i]

        output_path = "processed_audio.wav"
        processed_audio.export(output_path, format="wav")

        # Clean up the temporary segment files
        for seg_path in segments_paths:
            os.remove(seg_path)
            print(f"Segment file {seg_path} deleted.")
        # Remove the temporary directory if it's empty
        if not os.listdir(output_dir):
            os.rmdir(output_dir)
            print(f"Temporary directory {output_dir} deleted.")

        self.label.setText("Processing complete.")
        confirmation_dialog = ConfirmationDialog(output_path)
        confirmation_dialog.exec_()


    def closeEvent(self, event):
        super().closeEvent(event)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
