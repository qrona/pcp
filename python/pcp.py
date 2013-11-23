'''
PCP implementation.
To run tests:
python pcp.py --test
'''

import argparse
import numpy as np
import Tkinter
from PIL import Image, ImageTk
import scipy.io as sio


def animate(csv_file, w, h):
    tk_win = Tkinter.Tk()
    tk_win.title('Escalator')
    canvas = Tkinter.Canvas(tk_win, width=w, height=h)
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
    # mu = (n1 * n2) / float(4 * np.max(np.sum(np.abs(matrix), axis=0)))
    lbda = 1e-2
    mu = 1e-4

    iter = 1
    while True:
        # import pdb ; pdb.set_trace()
        print("-"*10 + "Iteration %d" % (iter) + "-"*10)
        iter += 1
        U, evs, V = np.linalg.svd(matrix - S - ((1/mu) * Y))
        # TODO : BUGGY np.diag
        eps = np.zeros(matrix.shape)
        eps[:matrix.shape[1], :matrix.shape[1]] = np.diag(thresh(evs, mu))
        L_new = np.dot(np.dot(U, eps), V)
        S_new = thresh(matrix - L_new + ((1/mu) * Y), lbda * mu)
        Y_new = Y + mu * (matrix - L_new - S_new)

        if converged(matrix, L_new, S_new):
            return L_new, S_new

        S = S_new
        Y = Y_new
        # import pdb ; pdb.set_trace()

#	return L_new, S_new


def test_pcp():
    def pcp_and_print(matrix):
        print 'M:'
        print matrix
        L, S = pcp(matrix)

        print 'L:'
        print L

        print 'S:'
        print S

        import pdb
        pdb.set_trace()

#	M = np.asarray([[10 for x in range(10)] for y in range(10)])
# pcp_and_print(M)
#
#	N = np.zeros((10, 10))
#	np.fill_diagonal(N, 5)
# pcp_and_print(N)
#
#	O = M
#	np.fill_diagonal(O, 5)
# import pdb ; pdb.set_trace()
    # M = sio.loadmat("escalator_data.mat")['X'] #10*np.asarray(np.ones((100,100)))
    # M = M[5000:10000,:]
    # import pdb ; pdb.set_trace()
    M = 10*np.ones((100, 100))
    m = np.random.rand(100, 100)
    m[m > 0.99] = 10.0
    m[m < 0.99] = 0
    M += m

    pcp_and_print(M)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--csv-file', dest='csv_file')

    parser.add_argument('--width', type=int, dest='width')
    parser.add_argument('--height', type=int, dest='height')
    parser.add_argument(
        '--animate', '-a', dest='animate', action='store_true', default=False)

    parser.add_argument(
        '--test', '-t', dest='test', action='store_true', default=False)

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
