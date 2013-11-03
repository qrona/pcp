'''
Convert a bmp file to a csv file
'''
import numpy as np
import scipy.io as sio
import sys
from PIL import Image

if __name__ == '__main__':
	im = Image.open(sys.argv[1]).convert('LA')
	matrix = np.array(im)
	np.savetxt('escalator_data.csv', matrix, delimiter = ',')