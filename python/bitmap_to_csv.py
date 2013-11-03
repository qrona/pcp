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
			im = Image.open(os.path.join(root, im_file)).convert('LA')
			pixels = list(im.getdata())

			matrix.append(pixels)

	np.savetxt('data.csv', np.array(matrix))
