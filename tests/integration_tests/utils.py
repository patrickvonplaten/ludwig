# -*- coding: utf-8 -*-
# Copyright (c) 2019 Uber Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import uuid

import pandas as pd

from ludwig.data.dataset_synthesyzer import build_synthetic_dataset

ENCODERS = [
    'embed', 'rnn', 'parallel_cnn', 'cnnrnn', 'stacked_parallel_cnn',
    'stacked_cnn'
]


def generate_data(
        input_features,
        output_features,
        filename='test_csv.csv',
        num_examples=25
):
    """
    Helper method to generate synthetic data based on input, output feature
    specs
    :param num_examples: number of examples to generate
    :param input_features: schema
    :param output_features: schema
    :param filename: path to the file where data is stored
    :return:
    """
    features = input_features + output_features
    df = build_synthetic_dataset(num_examples, features)
    data = [next(df) for _ in range(num_examples)]

    dataframe = pd.DataFrame(data[1:], columns=data[0])
    dataframe.to_csv(filename, index=False)

    return filename


def random_name(length=5):
    return uuid.uuid4().hex[:length].upper()


def numerical_feature(normalization=None):
    return {'name': 'num_' + random_name(), 'type': 'numerical',
            'preprocessing': {
                'normalization': normalization
            }
    }


def categorical_feature(**kwargs):
    cat_feature = {
        'type': 'category',
        'name': 'category_' + random_name(),
        'vocab_size': 10,
        'embedding_size': 5
    }

    cat_feature.update(kwargs)
    return cat_feature


def text_feature(**kwargs):
    feature = {
        'name': 'text_' + random_name(),
        'type': 'text',
        'reduce_input': 'null',
        'vocab_size': 5,
        'min_len': 7,
        'max_len': 7,
        'embedding_size': 8,
        'state_size': 8
    }
    feature.update(kwargs)
    return feature


def set_feature(**kwargs):
    feature = {
        'type': 'set',
        'name': 'set_' + random_name(),
        'vocab_size': 10,
        'max_len': 5,
        'embedding_size': 5
    }
    feature.update(kwargs)
    return feature


def sequence_feature(**kwargs):
    seq_feature = {
        'type': 'sequence',
        'name': 'sequence_' + random_name(),
        'vocab_size': 10,
        'max_len': 7,
        'encoder': 'embed',
        'embedding_size': 8,
        'fc_size': 8,
        'state_size': 8,
        'num_filters': 8
    }
    seq_feature.update(kwargs)
    return seq_feature


def image_feature(folder, **kwargs):
    img_feature = {
        'type': 'image',
        'name': 'image_' + random_name(),
        'encoder': 'resnet',
        'preprocessing': {
            'in_memory': True,
            'height': 8,
            'width': 8,
            'num_channels': 3
        },
        'resnet_size': 8,
        'destination_folder': folder,
        'fc_size': 8,
        'num_filters': 8
    }
    img_feature.update(kwargs)
    return img_feature

def audio_feature(folder, **kwargs):
    audio_feature = {
        'name': 'audio_' + random_name(),
        'type': 'audio',
        'preprocessing': {
            'audio_feature': {
                'type': 'raw',
            },
            'audio_file_length_limit_in_s': 3.0
        },
        'encoder': 'stacked_cnn',
        'should_embed': False,
        'conv_layers': [
            {
                'filter_size': 400,
                'pool_size': 16,
                'num_filters': 32,
                'regularize': 'false'
            },
            { 
                'filter_size': 40,
                'pool_size': 10,
                'num_filters': 64,
                'regularize': 'false'
            }
        ],
        'fc_size': 256,
        'audio_dest_folder': folder
    }
    audio_feature.update(kwargs)
    return audio_feature

def timeseries_feature(**kwargs):
    ts_feature = {
        'name': 'timeseries_' + random_name(),
        'type': 'timeseries',
        'max_len': 7
    }
    ts_feature.update(kwargs)
    return ts_feature


def binary_feature():
    return {
        'name': 'binary_' + random_name(),
        'type': 'binary'
    }


def bag_feature(**kwargs):
    feature = {
        'name': 'bag_' + random_name(),
        'type': 'bag',
        'max_len': 5,
        'vocab_size': 10,
        'embedding_size': 5
    }
    feature.update(kwargs)

    return feature
