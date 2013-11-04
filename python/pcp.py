'''
PCP implementation.
'''

import argparse
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


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('csv_file', metavar = 'csv-file')
	parser.add_argument('width', type = int)
	parser.add_argument('height', type = int)
	parser.add_argument('--animate', '-a', dest = 'animate', action = 'store_true', default = False)

	parsed = parser.parse_args()

	if parsed.animate:
		animate(parsed.csv_file, parsed.width, parsed.height)