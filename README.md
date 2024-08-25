# 💡 AUDIO AD BLOCKER
<!-- cool project cover image -->
![Project Cover Image](/media/audio_ad_blocker_image.jpg)

<!-- table of content -->
## Table of Contents
- [The Team](#the-team)
- [Project Description](#project-description)
  - [Problem Description](#problem-description)
  - [Solution](#solution)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
  - [Activation](#Activation)
- [Acknowledgments](#Acknowledgments)
- [References](#References)

## 👥 The Team 
### Team Members
- Odelia Harroch (odelia.harroch@mail.huji.ac.il)
- Ariel Erusalimsky (ariel.erusalimsky@mail.huji.ac.il)

### Supervisor
- Gal Katzhendler (gal.katzhendler@mail.huji.ac.il)


## 📚 Project Description
### 🔍 Problem Description

Audio Ad Blocker addresses the frustration many users face with frequent ad interruptions while streaming audio on platforms like Spotify, YouTube, and live radio. These disruptions diminish the listening experience, making it difficult to enjoy continuous content without interruptions.

### 💡 Solution
Our project is designed to effectively filter and remove advertisements from podcasts, whether they come from radio streams or other platforms. By utilizing advanced techniques in signal processing, deep learning, and machine learning, our solution quickly identifies and removes ads in near real-time, providing a smoother and more enjoyable listening experience across various audio sources.

#### Key Technologies Used
- **Deep Learning Embeddings:** We utilize deep learning models such as VGGish and OpenL3 to extract vector features from audio streams. These embeddings capture the essential characteristics of the audio, enabling the system to differentiate between content and advertisements.
- **Machine Learning Models:** We tested and trained various machine learning models, including K-Nearest Neighbors (KNN), Support Vector Machines (SVM), and Random Forest, using carefully curated datasets to accurately detect advertisements. After extensive evaluation, we selected the model that demonstrated the highest performance and accuracy.
- **User Interface:** A user-friendly interface built with PyQt5 allows users to easily interact with the system, offering both real-time and offline modes for seamless ad removal.

#### Modes of Operation
- **Real-Time Mode:** Filters out ads as users listen to live radio streams and other audio content, providing uninterrupted enjoyment.
- **Offline Mode:** Removes ads from pre-recorded podcasts, allowing users to download ad-free audio files.

#### Technologies Integrated:
- Python
- VGGish Model
- OpenL3 Model
- scikit-learn models (SVM, KNN, Random Forest)
  
This project aims to set a new standard for audio consumption worldwide, ensuring an enhanced experience for all users.

## ⚡Getting Started
### 🧱 Prerequisites
Ensure you have the following software and libraries installed to run the Audio Ad Blocker:
- **Python 3.7.11:** Python is the programming language used to develop this project. Ensure you have at version 3.7.11 installed.

- **numpy**: A fundamental package for scientific computing with Python, used for handling arrays and complex mathematical operations (pip install numpy).

- **TensorFlow 2.x:** TensorFlow is a deep learning framework essential for running the VGGish model, which we use for audio feature extraction
   (*pip install tensorflow*).
 - **tf_slim**: A lightweight library for defining, training, and evaluating complex models in TensorFlow (*pip install tf_slim*).
- **PyQt5:** PyQt5 is a set of Python bindings for the Qt application framework, used here to build the graphical user interface
   (*pip install pyqt5*).
  
- **pydub:** A Python library used for simple and easy manipulation of audio files. It handles audio file conversion, slicing, and processing tasks.
   (*pip install pydub*).  
- **pyaudio:** PyAudio allows the project to capture and process real-time audio streams, enabling the real-time ad-blocking functionality
   (*pip install pyaudio*).
- **soundfile**: A library for reading and writing sound files in different formats (e.g., WAV, FLAC).
- **resampy**: A Python library for audio and music processing, particularly for resampling audio signals (*pip install resampy*).  
- **joblib:** A library for efficient serialization and deserialization of Python objects, crucial for loading the pre-trained SVM model used in this project
   (*pip install joblib*).
- **nircmd:** A command-line utility that lets you control system volume, necessary for muting and unmuting audio during real-time ad filtering. Make sure to download the version that matches your OS (https://www.nirsoft.net/utils/nircmd.html).

- **scikit-learn:** A library for machine learning that provides simple and efficient tools for data mining and data analysis (pip install scikit-learn).
  
- **VGGish model file:** The VGGish model is pre-trained for extracting audio embeddings. Download the vggish_model.ckpt file from the official Google repository (https://github.com/tensorflow/models/blob/master/research/audioset/vggish).

### 🏗️ Installing 
To get started, follow these steps:

1. **Clone the Repository:** Download all the files in the "off&online audio processing" directory from the project repository.

2. **Set Up the Python Environment:** Ensure you have created and activated a Python environment. Install the required libraries mentioned in the Prerequisites section manually via the PyCharm terminal if necessary.

3. **Update the VGGish Model Path**: In the Vggish_Embeddings_Model file, update the path to the vggish_model.ckpt file to match the location where you saved it on your local system.

### 🚀 Activation
Once the installation steps are complete, follow these instructions to activate the application:

1. **Choose Your Mode:** Depending on whether you want to process audio in real-time or offline, navigate to either the "ONline" or "OFFline" directory.

2. **Run the Application:** Execute the appropriate Python script within your selected directory. Make sure to update the file paths in the code to match your local system’s directory structure.
  
## 🙏 Acknowledgments
We deeply thank our mentor, Gal Katzhendler, for his exceptional guidance, unwavering support, and insightful feedback, which were crucial to the success of this project. Special thanks to Prof. Daphna Weinshall, Yuri Klebanov, and Nir Sweed for their valuable advice and insights throughout the last year.

## 📘 References
[1] Look, Listen and Learn More: Design Choices for Deep Audio Embeddings
Aurora Cramer, Ho-Hsiang Wu, Justin Salamon, and Juan Pablo Bello.
IEEE Int. Conf. on Acoustics, Speech and Signal Processing (ICASSP), pages 3852-3856, Brighton, UK, May 2019.

[2] Look, Listen and Learn
Relja Arandjelović and Andrew Zisserman
IEEE International Conference on Computer Vision (ICCV), Venice, Italy, Oct. 2017.

[3] https://github.com/tensorflow/models/blob/master/research/audioset/vggish

[4] https://www.nirsoft.net/utils/nircmd.html



