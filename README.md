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

Introducing Audio Ad Blocker, our innovative project designed to transform the audio streaming experience. Today, platforms like Spotify and YouTube are primary sources of entertainment and information. However, users often face frustration due to frequent ad interruptions that disrupt their listening pleasure.

### 💡 Solution

Our solution integrates advanced techniques from signal processing, deep learning, machine learning, and software development. Leveraging these technologies, we aim to efficiently identify and remove advertisements from audio streams in near real-time.

- **Deep Learning Embeddings:** We used a deep learning model to produce embeddings, which are vector features of the audio.
- **Machine Learning Models:** To accurately detect advertisements, we trained various machine learning models using suitable datasets we created. We then selected the model with the best performance and accuracy.
To make this solution accessible, we have developed a user-friendly interface with two modes of operation:

- **Real-Time Mode:** Users can connect to the interface while listening to audio content, allowing it to filter out ads as they play.
- **Offline Mode:** Users can upload podcast files to the interface for ad removal, then download the processed file free of ads.
This project aims to set a new standard for audio consumption worldwide, ensuring an enhanced experience for all users.

## ⚡Getting Started
### 🧱 Prerequisites
Ensure you have the following software and libraries installed to run the Audio Ad Blocker:
- **Python 3.7.11:** Python is the programming language used to develop this project. Ensure you have at version 3.7.11 installed

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
  
- **VGGish model file:** The VGGish model is pre-trained for extracting audio embeddings. Download the vggish_model.ckpt file from the official Google repository (https://github.com/tensorflow/models/blob/master/research/audioset/vggish).

### 🏗️ Installing 
To get started, follow these steps:

1. **Clone the Repository:**: Download all the files in the "off&online audio processing" directory from the project repository.

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



