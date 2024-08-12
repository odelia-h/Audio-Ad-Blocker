import pyaudio
import wave
import math
import numpy as np
import os
import joblib
import threading
import queue
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from pydub import AudioSegment
from Vggish_Embeddings_Model import extract_vggish_embeddings

class AudioProcessor:
    def __init__(self, svm_model_path):
        self.svm_model = joblib.load(svm_model_path)

    def convert_to_embeddings(self, file_path):
        embeddings = extract_vggish_embeddings(file_path)
        print(f"Embeddings extracted: {embeddings.shape}")
        return embeddings

    def detect_ads(self, file_path):
        embedding = self.convert_to_embeddings(file_path)
        prediction = self.svm_model.predict([embedding])
        return prediction == 1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-Time Ad Detector")
        self.audio_processor = AudioProcessor('svm_model_vggish_5sec_alldata.pkl')

        self.label = QLabel("Press 'Start' to begin real-time ad detection...")
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_detection)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_detection)
        self.stop_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.is_running = False
        self.audio_queue = queue.Queue()

    def start_detection(self):
        self.is_running = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.capture_thread = threading.Thread(target=self.capture_audio)
        self.process_thread = threading.Thread(target=self.process_audio)

        self.capture_thread.start()
        self.process_thread.start()

    def stop_detection(self):
        self.is_running = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.label.setText("Detection stopped.")

        self.capture_thread.join()
        self.process_thread.join()

    def capture_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        while self.is_running:
            frames = []

            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            wave_file_path = "temp_audio.wav"
            wf = wave.open(wave_file_path, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            self.audio_queue.put(wave_file_path)

        stream.stop_stream()
        stream.close()
        p.terminate()

        print("* done recording")

    def process_audio(self):
        while self.is_running or not self.audio_queue.empty():
            try:
                wave_file_path = self.audio_queue.get(timeout=1)
            except queue.Empty:
                continue

            print(f"Processing file: {wave_file_path}")
            audio = AudioSegment.from_wav(wave_file_path)

            duration_ms = len(audio)
            print(f"Audio duration: {duration_ms} ms")
            segment_duration_ms = 5000
            num_segments = math.ceil(duration_ms / segment_duration_ms)
            print(f"Number of segments: {num_segments}")

            output_dir = "audio_segments"
            os.makedirs(output_dir, exist_ok=True)
            segments_paths = []
            seg_list = []
            for i in range(num_segments):
                start_time = i * segment_duration_ms
                end_time = min(start_time + segment_duration_ms, duration_ms)
                segment = audio[start_time:end_time]
                seg_list.append(segment)
                segment_path = os.path.join(output_dir, f"segment_{i + 1}.wav")
                segment.export(segment_path, format="wav")
                segments_paths.append(segment_path)
                print(f"Segment {i + 1} saved: {segment_path}")

            detected_ad = False

            for seg_path in segments_paths:
                if self.audio_processor.detect_ads(seg_path):
                    detected_ad = True
                    break

            if detected_ad:
                self.mute_system_volume()
                self.label.setText("Ad detected! Muting system volume...")
            else:
                self.restore_system_volume()
                self.label.setText("No ad detected. Volume restored.")

            for seg_path in segments_paths:
                os.remove(seg_path)
                print(f"Segment file {seg_path} deleted.")

            if not os.listdir(output_dir):
                os.rmdir(output_dir)
                print(f"Temporary directory {output_dir} deleted.")

            os.remove(wave_file_path)
            print(f"Temporary audio file {wave_file_path} deleted.")

    def mute_system_volume(self):
        try:
            if sys.platform == "win32":
                os.system("C:/Users/odeli/PycharmProjects/pythonProject1/nircmd-x64/nircmd.exe mutesysvolume 1")
                print("mute")
            elif sys.platform == "darwin":
                os.system("osascript -e 'set volume output muted true'")
            elif sys.platform == "linux":
                os.system("amixer set Master mute")
        except Exception as e:
            print(f"Error muting system volume: {e}")

    def restore_system_volume(self):
        try:
            if sys.platform == "win32":
                os.system("C:/Users/odeli/PycharmProjects/pythonProject1/nircmd-x64/nircmd.exe mutesysvolume 0")
                print("unmute")
            elif sys.platform == "darwin":
                os.system("osascript -e 'set volume output muted false'")
            elif sys.platform == "linux":
                os.system("amixer set Master unmute")
        except Exception as e:
            print(f"Error restoring system volume: {e}")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
