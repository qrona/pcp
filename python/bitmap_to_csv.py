'''
Convert a bmp file to a csv file
'''
import numpy as np
import os
import scipy.io as sio
import sys
from PIL import Image

if __name__ == '__main__':
	images_dir = sys.argv[1]
	matrix = []
	for root, dirs, files in os.walk(images_dir):
		for im_file in files:
			im = Image.open(os.path.join(root, im_file)).convert('L')
			pixels = list(im.getdata())

			matrix.append(pixels)
        arres = np.array(matrix)

	np.savetxt('data.csv', arres)
