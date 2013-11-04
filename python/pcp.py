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

def pcp(matrix):
	def converged(M, L, S):
		return np.linalg.norm(M - L - S) <= (10 ** -7) * np.linalg.norm(M)

	def thresh(A, t):

		def thresh_element(x):
			return np.sign(x) * max([abs(x) - t, 0])

		f = np.vectorize(thresh_element)
		return f(A)

	S = np.zeros(matrix.shape)
	Y = np.zeros(matrix.shape)
	n1, n2 = matrix.shape
	mu = (n1 * n2) / float(4 * np.max(np.sum(np.abs(matrix), axis=0)))
	lbda = 1

	while True:
		U, evs, V = np.linalg.svd(matrix - S - ((1/mu) * Y))
		L_new = U * thresh(evs, mu) * V
		S_new = thresh(matrix - L_new + ((1/mu) * Y), mu * lbda)
		Y_new = Y + mu * (matrix - L_new - S_new)

		if converged(matrix, L_new, S_new):
			return L_new, S_new

		S = S_new
		Y = Y_new

def test_pcp():
	def pcp_and_print(matrix):
		print 'M:'
		print matrix
		L, S = pcp(matrix)

		print 'L:'
		print L

		print 'S:'
		print S

	M = np.asarray([[10 for x in range(10)] for y in range(10)])
	pcp_and_print(M)

	N = np.zeros((10, 10))
	np.fill_diagonal(N, 5)
	pcp_and_print(N)
	
	O = M
	np.fill_diagonal(O, 5)
	pcp_and_print(O)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('--csv-file', dest = 'csv_file')

	parser.add_argument('--width', type = int, dest = 'width')
	parser.add_argument('--height', type = int, dest = 'height')
	parser.add_argument('--animate', '-a', dest = 'animate', action = 'store_true', default = False)

	parser.add_argument('--test', '-t', dest = 'test', action = 'store_true', default = False)

	parsed = parser.parse_args()

	if parsed.animate:
		animate(parsed.csv_file, parsed.width, parsed.height)

	elif parsed.test:
		test_pcp()

	else:
		M = np.loadtxt(parsed.csv_file)
		L, S = pcp(M)
		print 'L:'
		print L

		print 'S:'
		print S