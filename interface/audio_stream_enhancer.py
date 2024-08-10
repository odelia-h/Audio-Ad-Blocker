import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QMessageBox, QFileDialog, QDesktopWidget, QGroupBox,
                             QProgressBar, QHBoxLayout, QMenuBar, QAction,
                             QStatusBar, QToolTip, QScrollArea)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QCoreApplication
import pygame

class AudioProcessingThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        for i in range(101):
            QThread.msleep(20)  # Simulate a time-consuming process
            self.progress.emit(i)
        self.finished.emit()

class AudioPlaybackThread(QThread):
    def __init__(self, audio_file):
        super().__init__()
        self.audio_file = audio_file
        self.paused = False
        self.last_position = 0

    def run(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(self.audio_file)
        if self.paused:
            pygame.mixer.music.play(start=self.last_position)
        else:
            pygame.mixer.music.play()

    def pause(self):
        if pygame.mixer.music.get_busy():
            self.paused = True
            self.last_position = pygame.mixer.music.get_pos()
            pygame.mixer.music.pause()

    def resume(self):
        if self.paused:
            self.paused = False
            pygame.mixer.music.unpause()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Stream Enhancer")
        self.setWindowIcon(QIcon('icon.png'))
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # Enable high DPI scaling

        self.uploaded_file = None  # Initialize the uploaded_file attribute

        self.default_stylesheet = """
            QWidget {
                background-color: #E4EBF2;
                color: #000000;
            }
            QMenuBar {
                background-color: #FFFFFF;
                color: #000000;
            }
            QMenuBar::item {
                background-color: #FFFFFF;
                color: #000000;
                padding: 4px 10px;
                border-radius: 5px;
            }
            QMenuBar::item:selected {
                background-color: #DDDDDD;
            }
            QGroupBox {
                background-color: #FFFFFF;
                border: 2px solid #328DAA;
                border-radius: 15px;
                padding: 20px;
                font-size: 36px;
                font-weight: bold;
                color: #000000;
            }
            QPushButton {
                padding: 20px;
                background-color: #328DAA;
                color: #FFFFFF;
                font-size: 36px;
                border-radius: 25px;
                text-align: center; 
            }
            QPushButton:hover {
                background-color: #2A7387;
            }
            QProgressBar {
                border: 2px solid #328DAA;
                border-radius: 5px;
                text-align: center;
                font-size: 28px;
                color: #5A4D4C;
            }
            QProgressBar::chunk {
                background-color: #8ED3F4;
            }
            QLabel {
                font-size: 32px;
                color: #5A4D4C;
                background-color: #FFFFFF;
                border: 1px solid #5A4D4C;
                border-radius: 10px;
                padding: 20px;
            }
            QToolTip {
                background-color: #328DAA;
                color: #FFFFFF;
                border: 1px solid #FFFFFF;
            }
            QStatusBar {
                font-size: 24px;
                color: #5A4D4C;
            }
        """
        self.dark_stylesheet = """
            QWidget {
                background-color: #2B2B2B;
                color: #F0F0F0;
            }
            QMenuBar {
                background-color: #3F3F3F;
                color: #F0F0F0;
            }
            QMenuBar::item {
                background-color: #3F3F3F;
                color: #F0F0F0;
                padding: 4px 10px;
                border-radius: 5px;
            }
            QMenuBar::item:selected {
                background-color: #535353;
            }
            QGroupBox {
                background-color: #3F3F3F;
                border: 2px solid #328DAA;
                border-radius: 15px;
                padding: 20px;
                font-size: 36px;
                font-weight: bold;
                color: #F0F0F0;
            }
            QPushButton {
                padding: 20px;
                background-color: #328DAA;
                color: #FFFFFF;
                font-size: 36px;
                border-radius: 25px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #2A7387;
            }
            QProgressBar {
                border: 2px solid #328DAA;
                border-radius: 5px;
                text-align: center;
                font-size: 28px;
                color: #F0F0F0;
            }
            QProgressBar::chunk {
                background-color: #8ED3F4;
            }
            QLabel {
                font-size: 32px;
                color: #F0F0F0;
                background-color: #3F3F3F;
                border: 1px solid #5A4D4C;
                border-radius: 10px;
                padding: 20px;
            }
            QToolTip {
                background-color: #328DAA;
                color: #FFFFFF;
                border: 1px solid #FFFFFF;
            }
            QStatusBar {
                font-size: 24px;
                color: #F0F0F0;
            }
        """
        self.setStyleSheet(self.default_stylesheet)
        self.init_ui()
        self.center_window()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Menu Bar
        menu_bar = QMenuBar()
        settings_menu = menu_bar.addMenu('Settings')
        help_menu = menu_bar.addMenu('Help')

        theme_action = QAction('Change Theme', self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_action)

        help_action = QAction('Help', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        main_layout.addWidget(menu_bar)

        # Header
        header_layout = QVBoxLayout()
        self.header_label = QLabel("Welcome to Audio Ad Blocker")
        self.header_label.setStyleSheet("font-size: 42px; font-weight: bold; color: #5A4D4C;")
        self.header_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.header_label)

        header_image = QLabel()
        header_image.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap('header_image.jpg')
        scaled_pixmap = pixmap.scaledToWidth(400, Qt.SmoothTransformation)
        header_image.setPixmap(scaled_pixmap)
        header_layout.addWidget(header_image, alignment=Qt.AlignCenter)

        main_layout.addLayout(header_layout)

        # Scroll Area for Main Content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Instructions Group Box
        self.instructions_group = QGroupBox()
        instructions_layout = QVBoxLayout()

        title_label = QLabel("Instructions")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #328DAA;")
        instructions_layout.addWidget(title_label)

        instructions_text = QLabel()
        instructions_text.setText("<ol>"
                                  "<li>Click <b>'Upload Audio File'</b> to select an audio file from your computer.</li>"
                                  "<li>Click <b>'Process Audio'</b> to remove advertisements from the uploaded audio.</li>"
                                  "<li>Click <b>'Play Audio'</b> to listen to the processed audio.</li>"
                                  "<li>Click <b>'Download Audio'</b> to save the processed audio to your computer.</li>"
                                  "</ol>")
        instructions_text.setWordWrap(True)
        instructions_layout.addWidget(instructions_text)
        self.instructions_group.setLayout(instructions_layout)
        scroll_layout.addWidget(self.instructions_group)

        # Ensure there is vertical spacing
        scroll_layout.addSpacing(20)  # Adjust the value as needed for more or less space

        # Progress Bar
        self.progress_bar = QProgressBar()
        scroll_layout.addWidget(self.progress_bar)

        # Ensure more vertical spacing after the progress bar if needed
        scroll_layout.addSpacing(20)  # Adjust as necessary

        # Buttons Layout
        buttons_layout = QVBoxLayout()

        # First Row of Buttons
        first_row_layout = QHBoxLayout()
        self.upload_button = QPushButton("Upload Audio File")
        self.upload_button.clicked.connect(self.upload_file)
        first_row_layout.addWidget(self.upload_button)

        self.process_button = QPushButton("Process Audio")
        self.process_button.clicked.connect(self.process_audio)
        first_row_layout.addWidget(self.process_button)

        buttons_layout.addLayout(first_row_layout)

        # Second Row of Buttons
        second_row_layout = QHBoxLayout()
        self.play_button = QPushButton("Play Audio")
        self.play_button.clicked.connect(self.play_audio)
        second_row_layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop Audio")
        self.stop_button.clicked.connect(self.stop_audio)  # Connect to stop_audio method
        second_row_layout.addWidget(self.stop_button)

        self.download_button = QPushButton("Download Audio")
        self.download_button.clicked.connect(self.download_audio)
        second_row_layout.addWidget(self.download_button)

        buttons_layout.addLayout(second_row_layout)

        scroll_layout.addLayout(buttons_layout)

        # Add scroll content to scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)

    def center_window(self):
        screen = QDesktopWidget().availableGeometry()
        size = self.sizeHint()
        self.resize(size)
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def upload_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Audio File", "", "Audio Files (*.wav *.mp3)", options=options)
        if file_name:
            self.uploaded_file = file_name  # Store the uploaded file path
            QMessageBox.information(self, "Success", f"File '{file_name}' uploaded successfully.")
        else:
            QMessageBox.warning(self, "Error", "File upload failed.")

    def process_audio(self):
        if not self.uploaded_file:
            QMessageBox.warning(self, "Error", "No audio file uploaded.")
            return

        # Simulate processing
        self.audio_thread = AudioProcessingThread()
        self.audio_thread.progress.connect(self.update_progress)
        self.audio_thread.finished.connect(self.processing_finished)
        self.audio_thread.start()
        self.status_bar.showMessage("Processing...")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def processing_finished(self):
        QMessageBox.information(self, "Success", "Audio processing completed.")
        self.status_bar.showMessage("Processing completed.")

    def play_audio(self):
        if not self.uploaded_file:
            QMessageBox.warning(self, "Error", "No audio file uploaded.")
            return

        if hasattr(self, 'audio_playback_thread'):
            self.audio_playback_thread.resume()
        else:
            self.audio_playback_thread = AudioPlaybackThread(self.uploaded_file)
            self.audio_playback_thread.start()

    def stop_audio(self):
        if hasattr(self, 'audio_playback_thread'):
            self.audio_playback_thread.pause()

    def download_audio(self):
        if not self.uploaded_file:
            QMessageBox.warning(self, "Error", "No audio file uploaded.")
            return
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Processed Audio", "", "Audio Files (*.wav *.mp3)", options=options)
        if file_name:
            QMessageBox.information(self, "Success", f"Processed audio saved as '{file_name}' (simulated).")
        else:
            QMessageBox.warning(self, "Error", "File save failed.")

    def toggle_theme(self):
        current_style = self.styleSheet()
        if current_style == self.default_stylesheet:
            self.setStyleSheet(self.dark_stylesheet)
            self.header_label.setStyleSheet("font-size: 42px; font-weight: bold; color: #FFFFFF;")  # Change to white for dark mode
        else:
            self.setStyleSheet(self.default_stylesheet)
            self.header_label.setStyleSheet("font-size: 42px; font-weight: bold; color: #5A4D4C;")  # Change back to original color for default mode

    def show_help(self):
        help_message = QMessageBox(self)
        help_message.setWindowTitle("Help")
        help_message.setText("This is a help message.")
        help_message.exec_()

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
