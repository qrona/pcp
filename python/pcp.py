'''
PCP implementation.
'''

import argparse
import numpy as np
import Tkinter
from PIL import Image, ImageTk

def animate(csv_file, w, h):
	tk_win = Tkinter.Tk()
	tk_win.title('Escalator')
	canvas = Tkinter.Canvas(tk_win, width = w, height = h)
	canvas.pack()

	has_more = True

	with open(csv_file, 'r') as csv_file_handle:
		for new_line in csv_file_handle:
			im = Image.new('L', (w, h))

			bitmap = map(float, new_line.split())
			im.putdata(bitmap)
			tk_im = ImageTk.PhotoImage(im)

			canvas.create_image(w, h, image=tk_im)
			canvas.update()

def pcp(csv_file):
	def converged(M, L, S):
		return True

	def thresh(A, t):
		return np.asarray([np.sign(x) * max([abs(x) - t, 0]) for x in A])

	with open(csv_file, 'r') as csv_file_handle:
		matrix = np.loadtxt(csv_file_handle)

		S = np.zeros(matrix.shape)
		Y = np.zeros(matrix.shape)
		n1, n2 = matrix.shape
		u = (n1 * n2) / (4 * np.max(np.sum(np.abs(matrix), axis=0)))
		l = 1

		while True:
			U, d, V = np.linalg.svd(matrix - S - ((1/u) * Y))
			import ipdb
			ipdb.set_trace()
			L_new = U * thresh(d, l * u) * V
			S_new = S
			Y_new = Y + u * (matrix - L_new - S_new)

			if converged(matrix, L_new, S_new):
				return L_new, S_new

			S = S_new
			Y = Y_new

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('csv_file', metavar = 'csv-file')
	parser.add_argument('width', type = int)
	parser.add_argument('height', type = int)
	parser.add_argument('--animate', '-a', dest = 'animate', action = 'store_true', default = False)

	parsed = parser.parse_args()

	if parsed.animate:
		animate(parsed.csv_file, parsed.width, parsed.height)
	else:
		pcp(parsed.csv_file)