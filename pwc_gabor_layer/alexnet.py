# AUTOGENERATED! DO NOT EDIT! File to edit: 01_alexnet.ipynb (unless otherwise specified).

__all__ = ['GaborBlock', 'AlexNet']

# Cell
from .core import GaborLayer, SigmaRegularizer
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Cell
class GaborBlock(keras.Model):
    def __init__(self, filters_gabor, filters_conv,  kernel_size,
                 learn_orientations=False, strides=(1, 1),
                 padding='SAME', sigma_regularizer=None, **kwargs):
        super().__init__(**kwargs)

        self.gabor_layer = GaborLayer(filters=filters_gabor,
                                      kernel_size=kernel_size,
                                      sigma_regularizer=sigma_regularizer,
                                      learn_orientations=learn_orientations,
                                      use_bias=False,
                                      orientations=8,
                                      activation='relu',
                                      strides=strides,
                                      padding=padding)

        self.conv_layer = keras.layers.Conv2D(filters=filters_conv,
                                              kernel_size=(1, 1),
                                              use_bias=False,
                                              activation='relu')

    def call(self, x, training=False):
        x = self.gabor_layer(x)
        x = self.conv_layer(x)

        return x

# Cell
class AlexNet(keras.Model):
    def __init__(self, num_classes=10, input_channels=3,
                kernels1=None, kernels2=None, kernels3=None,
                learn_orientations=False, **kwargs):
        super().__init__(*kwargs)

        self.learn_orientations = learn_orientations
        self.num_classes = num_classes
        self.input_channels = input_channels

        self.conv1 = self.add_conv_layer(kernels1, 96, (11, 11), strides=4)
        self.conv2 = self.add_conv_layer(kernels2, 256, (5, 5), strides=1)
        self.conv3 = self.add_conv_layer(kernels3, 384, (3, 3), strides=1)

        # Define further conv layers:

        self.conv4 = self.add_conv_layer(None, 384, (3, 3), strides=1)
        self.conv5 = self.add_conv_layer(None, 256, (3, 3), strides=1)

        # Define output (dense connections)
        self.linear1 = keras.layers.Dense(512, activation='relu')
        self.linear2 = keras.layers.Dense(512, activation='relu')
        self.linear3 = keras.layers.Dense(self.num_classes, activation='sigmoid')

        # Supporting layers
        self.maxpool = keras.layers.MaxPooling2D()
        self.dropout = keras.layers.Dropout(0.5)
        self.flatten = keras.layers.Flatten()

    def call(self, x, training=False):
        # block 1
        x = self.conv1(x)
        x = self.maxpool(x)
        # block 2
        x = self.conv2(x)
        x = self.maxpool(x)
        # block 3
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.maxpool(x)
        # classifier
        x = self.flatten(x)
        x = self.linear1(x)

        if training:
            x = self.dropout(x)

        x = self.linear2(x)

        if training:
            x = self.dropout(x)

        x = self.linear3(x)

        return x


    def add_conv_layer(self, gabor, filters_conv, kernel_size, strides):

        if gabor:
            block = GaborBlock(filters_gabor=gabor,
                                    filters_conv=filters_conv,
                                    kernel_size=kernel_size,
                                    strides=strides,
                                    learn_orientations=self.learn_orientations)
        else:
            block = keras.layers.Conv2D(filters=filters_conv,
                                       kernel_size=kernel_size,
                                       strides=strides,
                                       activation='relu',
                                       padding='same')
        return block
