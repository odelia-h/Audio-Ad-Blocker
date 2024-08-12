import os
import sys
import numpy as np
import tensorflow as tf
import vggish_input
import vggish_params
import vggish_postprocess
import vggish_slim

tf.compat.v1.disable_eager_execution()

# Set the directory containing VGGish model files
vggish_model_dir = "C:/Users/odeli/PycharmProjects/pythonProject1"  # Adjust this path

# Add VGGish model directory to Python path
sys.path.append(vggish_model_dir)

# Load the pre-trained VGGish modp.]
sess = tf.compat.v1.Session()
vggish_slim.define_vggish_slim(training=False)
vggish_slim.load_vggish_slim_checkpoint(sess, os.path.join(vggish_model_dir, 'vggish_model.ckpt'))

def convert_to_2d_array(three_d_array):
    # Get the dimensions of the input array
    #depth, rows, cols = three_d_array.shape
    print("vggish embedding", three_d_array)
    print("vggish shape",three_d_array.shape)

    # Reshape each 2D array to 1D and concatenate them
    flattened_arrays = [matrix.flatten() for matrix in three_d_array]
    two_d_array = np.vstack(flattened_arrays)

    return two_d_array

def extract_vggish_embeddings(audio_file): #, sample_rate=22050
    # Preprocess the numpy array into Mel spectrograms
    mel_features = vggish_input.wavfile_to_examples(audio_file)

    # Run VGGish model on preprocessed audio
    embedding_batch = sess.run('vggish/embedding:0',
                               feed_dict={'vggish/input_features:0': mel_features})
    #flattened_embeddings = convert_to_2d_array(embedding_batch)

    # Flatten the embeddings to fit the SVC model input
    flattened_embeddings = embedding_batch.flatten()

    print("final shape ", flattened_embeddings.shape)
    # Load the pre-trained VGGish model

    return flattened_embeddings


# def extract_vggish_embeddings(audio_buffer, sample_rate=22050):
#     # Preprocess the numpy array into Mel spectrograms
#     mel_features = vggish_input.waveform_to_examples(audio_buffer, sample_rate)
#
#     # Run VGGish model on preprocessed audio
#     embedding_batch = sess.run('vggish/embedding:0',
#                                feed_dict={'vggish/input_features:0': mel_features})
#     # Flatten the embeddings to fit the SVC model input
#     flattened_embeddings = embedding_batch.flatten()
#
#     return flattened_embeddings




