# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

import os
import glob

from paddleseg.datasets import Dataset
from paddleseg.cvlibs import manager
from paddleseg.transforms import Compose


@manager.DATASETS.add_component
class Mapillary(Dataset):

    NUM_CLASSES = 9
    IGNORE_INDEX = 255
    IMG_CHANNELS = 3

    def __init__(self, transforms, dataset_root, mode='train', edge=False):
        self.dataset_root = dataset_root
        self.transforms = Compose(transforms)
        self.file_list = list()
        mode = mode.lower()
        self.mode = mode
        self.num_classes = self.NUM_CLASSES
        self.ignore_index = self.IGNORE_INDEX
        self.edge = edge

        if mode not in ['training', 'validation', 'testing']:
            raise ValueError(
                "mode should be 'training', 'validation' or 'testing', but got {}.".format(
                    mode))

        if self.transforms is None:
            raise ValueError("`transforms` is necessary, but it is None.")

        img_files = sorted(glob.glob(os.path.join(dataset_root, mode, 'images', '*.jpg')))
        label_files = sorted(glob.glob(os.path.join(dataset_root, mode, 'labels', '*.png')))

        self.file_list = [
            [img_path, label_path]
            for img_path, label_path in zip(img_files, label_files)
        ]

