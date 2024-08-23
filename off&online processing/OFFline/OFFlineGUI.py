import math
import sys
import os
import joblib
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QFrame, QSlider, QStatusBar
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pydub import AudioSegment

from Vggish_Embeddings_Model import extract_vggish_embeddings


class AudioProcessor:
    """
    Class for processing audio and detecting ads using a pre-trained SVM model.
    """
    def __init__(self, svm_model_path):
        """
        Initialize the AudioProcessor with a pre-trained SVM model.

        :param svm_model_path: Path to the SVM model file.
        """
        self.svm_model = joblib.load(svm_model_path)

    def convert_to_embeddings(self, file_path):
        """
        Convert an audio file to VGGish embeddings.

        :param file_path: Path to the audio file.
        :return: Embeddings of the audio file.
        """
        embeddings = extract_vggish_embeddings(file_path)
        return embeddings

    def detect_ads(self, file_path):
        """
        Detect ads in the given audio file based on the embeddings.

        :param file_path: Path to the audio file.
        :return: True if ads are detected, False otherwise.
        """
        embedding = self.convert_to_embeddings(file_path)
        prediction = self.svm_model.predict([embedding])
        return prediction == 1


class MainWindow(QMainWindow):
    """
    Main window for the Audio Ad Blocker application.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Ad Blocker")
        self.setFixedSize(1400, 1000)  # Increased window size for better visibility

        # Set the color palette for the application window
        self.set_palette()

        self.audio_processor = AudioProcessor('svm_model_vggish_5sec.pkl')

        # Header Area
        self.header_label = QLabel("Audio Ad Blocker")
        self.header_label.setFont(QFont("Open Sans", 24, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)

        # Image Area
        self.image_label = QLabel()
        pixmap = QPixmap("header_image.jpg").scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Resize the image to a reasonable size
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Instructions Area with Styled Frame and Background
        self.instructions_frame = QFrame()
        self.instructions_frame.setFrameShape(QFrame.StyledPanel)
        self.instructions_frame.setStyleSheet("background-color: #f0f8ff; border: 2px solid #329daa; border-radius: 10px; padding: 10px;")
        self.instructions_label = QLabel(
            "Instructions:\n1. Click 'Upload Audio' to select an audio file.\n"
            "2. Click 'Process Audio' to remove ads from the selected audio file.\n"
            "3. Click 'Play/Pause' to listen to the ad-free audio."
        )
        self.instructions_label.setFont(QFont("Open Sans", 14, QFont.Bold))  # Enlarged the font size
        self.instructions_label.setAlignment(Qt.AlignLeft)  # Align text to the left
        self.instructions_label.setWordWrap(True)  # Allow text to wrap within the label
        self.instructions_label.setStyleSheet("line-height: 130%;")  # Spacing lines in the instructions
        instructions_layout = QVBoxLayout()
        instructions_layout.addWidget(self.instructions_label)
        self.instructions_frame.setLayout(instructions_layout)

        # Buttons with Styling
        button_style = """
        QPushButton {
            background-color: #329daa;
            color: white;
            border-radius: 15px;
            padding: 10px;
            min-width: 150px;
        }
        QPushButton:hover {
            background-color: #8ed3f4;
        }
        """
        self.upload_button = QPushButton("Upload Audio")
        self.upload_button.setStyleSheet(button_style)
        self.upload_button.setFont(QFont("Open Sans", 16, QFont.Bold))
        self.upload_button.clicked.connect(self.upload_audio)

        self.process_button = QPushButton("Process Audio")
        self.process_button.setStyleSheet(button_style)
        self.process_button.setFont(QFont("Open Sans", 16, QFont.Bold))
        self.process_button.clicked.connect(self.process_audio)

        # Play/Pause button
        self.play_pause_button = QPushButton("Play/Pause")
        self.play_pause_button.setStyleSheet(button_style)
        self.play_pause_button.setFont(QFont("Open Sans", 16, QFont.Bold))
        self.play_pause_button.clicked.connect(self.toggle_play_pause)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Message Area without Frame but with Different Text Color
        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Open Sans", 14))
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: #329daa;")  # Different color for messages

        # Media player and volume slider
        self.media_player = QMediaPlayer(None, QMediaPlayer.LowLatency)
        self.media_player.setVolume(50)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.media_player.setVolume)

        # Layout for the main window
        layout = QVBoxLayout()
        layout.addWidget(self.header_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.instructions_frame)

        # Button Layout (side by side)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.play_pause_button)  # Changed from play_button to play_pause_button
        layout.addLayout(button_layout)

        layout.addSpacing(20)
        layout.addWidget(self.message_label, alignment=Qt.AlignCenter)

        layout.addWidget(self.volume_slider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize variables
        self.file_path = None
        self.output_path = None
        #self.is_playing = False  # Track the playing state

    def set_palette(self):
        """
        Set the color palette for the application window.
        """
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#e4ebf2"))
        self.setPalette(palette)

    def upload_audio(self):
        """
        Upload an audio file through a file dialog and display its name.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Upload Audio", "",
                                                        "Audio Files (*.wav *.mp3);;All Files (*)", options=options)
        if self.file_path:
            self.message_label.setText(f"File uploaded: {os.path.basename(self.file_path)}")

    def process_audio(self):
        """
        Process the uploaded audio file by segmenting it, detecting ads, and saving the ad-free version.
        """
        if not self.file_path:
            self.message_label.setText("Please upload an audio file first.")
            self.statusBar.showMessage("No audio file uploaded", 3000)
            return

        audio = AudioSegment.from_file(self.file_path)

        # Determine the duration of the audio in milliseconds
        duration_ms = len(audio)
        segment_duration_ms = 5000
        num_segments = math.ceil(duration_ms / segment_duration_ms)
        output_dir = "audio_segments"
        os.makedirs(output_dir, exist_ok=True)
        segments_paths = []
        seg_list = []

        # Segment the audio file into smaller chunks for processing
        for i in range(num_segments):
            start_time = i * segment_duration_ms
            end_time = min(start_time + segment_duration_ms, duration_ms)
            segment = audio[start_time:end_time]
            if len(segment) < 5000:
                continue
            seg_list.append(segment)
            segment_path = os.path.join(output_dir, f"segment_{i + 1}.wav")
            segment.export(segment_path, format="wav")
            segments_paths.append(segment_path)

        # Combine non-ad segments into a single processed audio file
        processed_audio = AudioSegment.silent(duration=0)

        for i, seg_path in enumerate(segments_paths):
            if not self.audio_processor.detect_ads(seg_path):
                processed_audio += seg_list[i]

        # Save the processed audio to a file
        self.output_path = "processed_audio.wav"
        processed_audio.export(self.output_path, format="wav")

        self.message_label.setText("Processing complete. Processed audio saved.")

        # Clean up temporary segment files
        for seg_path in segments_paths:
            os.remove(seg_path)
        if not os.listdir(output_dir):
            os.rmdir(output_dir)

        self.statusBar.showMessage("Audio processing completed", 3000)

    def toggle_play_pause(self):
        """
        Toggle between playing and pausing the processed audio file.
        """
        if not self.output_path:
            self.message_label.setText("Please process the audio first.")
            self.statusBar.showMessage("No processed audio available", 3000)
            return

        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_pause_button.setText("Play")
            self.message_label.setText("Audio paused.")
            self.statusBar.showMessage("Audio paused", 3000)
        else:
            if self.media_player.mediaStatus() == QMediaPlayer.NoMedia:
                media_content = QMediaContent(QUrl.fromLocalFile(self.output_path))
                self.media_player.setMedia(media_content)
            self.media_player.play()
            self.play_pause_button.setText("Pause")
            self.message_label.setText("Playing audio...")
            self.statusBar.showMessage("Playing processed audio", 3000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
