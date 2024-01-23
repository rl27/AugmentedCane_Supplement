
# Calculate mean/std of dataset

# https://discuss.pytorch.org/t/discussion-why-normalise-according-to-imagenet-mean-and-std-dev-for-transfer-learning/115670
# https://github.com/Nikronic/CoarseNet/blob/master/utils/preprocess.py#L142-L200

# The below stats are in BGR channel order

# SIDEGUIDE
# [0.53754861 0.5585039  0.56620585] [0.32905903 0.34946867 0.36147153] <-- fst_moment & snd_moment of entire dataset
# ['0.5375415555595128', '0.5585023975438654', '0.5662081428643264'] <-- mean
# ['0.20025701669519042', '0.19376334014347402', '0.20220217337395466'] <-- std

# MAPILLARY
# ['0.47001511327876866', '0.45848799369258997', '0.4193367232397572'] train mean
# ['0.303481909223667', '0.27538533107529745', '0.2642387504621635'] train std
# ['0.470340842790945', '0.45873165805675514', '0.4196077196683413'] train + val mean
# ['0.3033709867177536', '0.27515901794741515', '0.2641164284669083'] train + val std
# ['0.47198877427366637', '0.4606297362810356', '0.42173671955562864'] train + val + test mean
# ['0.303473803383662', '0.2754372728633572', '0.264646402457512'] train + val + test std


from PIL import Image
import cv2
import numpy as np
import os

imagedir = 'training/images'
imagedir2 = 'validation/images'
imagedir3 = 'testing/images'

cnt = 0
c2 = 0
fst_moment = np.zeros(3)
snd_moment = np.zeros(3)

for subdir, dirs, files in os.walk(imagedir):
    for file in files:
        filepath = os.path.join(subdir, file)
        
        # cv2.imread
        asdf = cv2.imread(filepath) / 255
        sum_ = np.sum(asdf, axis=(0,1))
        sum_sq = np.sum(asdf**2, axis=(0,1))

        num_pixels = asdf.shape[0] * asdf.shape[1]

        fst_moment = (cnt * fst_moment + sum_) / (cnt + num_pixels)
        snd_moment = (cnt * snd_moment + sum_sq) / (cnt + num_pixels)

        cnt += num_pixels
        c2 += 1
        # if c2 % 50 == 0:
        #     print(c2, fst_moment, snd_moment, np.sqrt(snd_moment - fst_moment ** 2))

print(repr(fst_moment.astype(str)))
print(repr(np.sqrt(snd_moment - fst_moment ** 2).astype(str)))
for subdir, dirs, files in os.walk(imagedir2):
    for file in files:
        filepath = os.path.join(subdir, file)
        
        # cv2.imread
        asdf = cv2.imread(filepath) / 255
        sum_ = np.sum(asdf, axis=(0,1))
        sum_sq = np.sum(asdf**2, axis=(0,1))

        num_pixels = asdf.shape[0] * asdf.shape[1]

        fst_moment = (cnt * fst_moment + sum_) / (cnt + num_pixels)
        snd_moment = (cnt * snd_moment + sum_sq) / (cnt + num_pixels)

        cnt += num_pixels
        c2 += 1
        # if c2 % 50 == 0:
        #     print(c2, fst_moment, snd_moment, np.sqrt(snd_moment - fst_moment ** 2))

print(repr(fst_moment.astype(str)))
print(repr(np.sqrt(snd_moment - fst_moment ** 2).astype(str)))
for subdir, dirs, files in os.walk(imagedir3):
    for file in files:
        filepath = os.path.join(subdir, file)
        
        # cv2.imread
        asdf = cv2.imread(filepath) / 255
        sum_ = np.sum(asdf, axis=(0,1))
        sum_sq = np.sum(asdf**2, axis=(0,1))

        num_pixels = asdf.shape[0] * asdf.shape[1]

        fst_moment = (cnt * fst_moment + sum_) / (cnt + num_pixels)
        snd_moment = (cnt * snd_moment + sum_sq) / (cnt + num_pixels)

        cnt += num_pixels
        c2 += 1
        # if c2 % 50 == 0:
        #     print(c2, fst_moment, snd_moment, np.sqrt(snd_moment - fst_moment ** 2))

print(repr(fst_moment.astype(str)))
print(repr(np.sqrt(snd_moment - fst_moment ** 2).astype(str)))