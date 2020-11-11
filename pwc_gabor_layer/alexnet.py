# AUTOGENERATED! DO NOT EDIT! File to edit: 01_alexnet.ipynb (unless otherwise specified).

__all__ = ['GaborBlock', 'ConvBlock', 'AlexNet']

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

        self.max_pooling = keras.layers.MaxPool2D()


    def call(self, x, training=False):
        x = self.gabor_layer(x)
        x = self.conv_layer(x)
        x = self.max_pooling(x)

        return x

# Cell
class ConvBlock(keras.Model):
    def __init__(self, filters, kernel_size,strides=(1, 1),
                 padding='SAME', **kwargs):
        super().__init__(**kwargs)

        self.conv_layer = keras.layers.Conv2D(filters=filters,
                                              kernel_size=(1, 1),
                                              activation='relu',
                                              padding=padding,
                                              strides=strides,
                                              )

        self.max_pooling = keras.layers.MaxPool2D()


    def call(self, x, training=False):
        x = self.conv_layer(x)
        x = self.max_pooling(x)

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

        if kernels1:
            self.conv1 = GaborBlock(filters_gabor=kernels1,
                                    filters_conv=96,
                                    kernel_size=(11, 11),
                                    strides=4,
                                    padding='SAME',
                                    learn_orientations=self.learn_orientations)
        else:
            self.conv1 = ConvBlock(filters=96,
                                   kernel_size=(11, 11),
                                   strides=4,
                                   padding='same')


    def call(self, x, training=False):

        x = self.conv1(x)

        return x