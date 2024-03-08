import os
import shutil
import numpy as np

# https://stackoverflow.com/a/53376979

# Filenames: a.wav, a+.wav, b.wav
original_audio = ['a', 'a+', 'b']

# Pitches to generate
pitches = np.arange(0.2, 1, 0.02)

# Assume a sampling rate of 44100 Hz
command = '"ffmpeg -i {0}.wav -af asetrate=44100*{1},aresample=44100,atempo=1/{1} {0}/{1}.wav"'

for n in original_audio:
	if os.path.isdir(n):
		shutil.rmtree(n)
	os.makedirs(n)

	# Generate pitched-down files
	for i in pitches:
		os.system(command.format(n, format(i, '.2f')))

	# Copy over original file
	shutil.copy('{}.wav'.format(n), '{}/{}.wav'.format(n, '1.00'))