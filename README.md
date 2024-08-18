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
- [Acknowledgments](#acknowledgments)

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

### 🧱 Prerequisites
Requirements for the software and the necessary libraries to install:  
-**Python 3.7.11:** Ensure you have Python 3.7 or later installed.  
-**TensorFlow 2.x:** Required for using the VGGish model.  
-**PyQt5:** For building the GUI application.  
-**pydub:** To handle audio processing.  
-**pyaudio:** For real-time audio capture and processing.  
-**joblib:** For loading the pre-trained SVM model.  
-**nircmd:** A utility for muting and unmuting system volume that matches your computer OS.  
-**Git:** For version control and pushing changes to GitHub.  
-**VGGish model file:** Download the vggish_model.ckpt file from the official repository.  

### 🏗️ Installing  
You will need to download all the files in the directory "off&online audio processing" in a python environment.  
Run either the python file in the ONline directory or in the OFFline directory according to the mode you wish to use.  
Don't forget to change the path to the one of your current computer directory in the running code.  

## 🙏 Acknowledgments
We deeply thank our mentor, Gal Katzhendler, for his exceptional guidance, unwavering support, and insightful feedback, which were crucial to the success of this project. Special thanks to Prof. Daphna Weinshall, Yuri Klebanov, and Nir Sweed for their valuable advice and insights throughout the last year.

## 📘 References 
[1] Look, Listen and Learn More: Design Choices for Deep Audio Embeddings
Aurora Cramer, Ho-Hsiang Wu, Justin Salamon, and Juan Pablo Bello.
IEEE Int. Conf. on Acoustics, Speech and Signal Processing (ICASSP), pages 3852-3856, Brighton, UK, May 2019.

[2] Look, Listen and Learn
Relja Arandjelović and Andrew Zisserman
IEEE International Conference on Computer Vision (ICCV), Venice, Italy, Oct. 2017.



