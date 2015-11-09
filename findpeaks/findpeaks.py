""" Searches for peaks in data

    History:
         -nov 2015: Janko Slavic, update
         -mar 2013: janko.slavic@fs.uni-lj.si
"""

import numpy as np


def findpeaks(x, spacing=10, limit=None):
    """Finds peaks in `x` which are of `spacing` width and >=`limit`.

    :param x: values
    :param spacing: minimum width for single peak
    :param limit: peaks should have value greater or equal
    :return:
    """
    peak_candidate = np.zeros(x.size - 2 * spacing - 2)
    peak_candidate[:] = True
    for s in range(spacing):
        h_b = x[s:-2 * spacing + s - 2]  # before
        h_c = x[spacing: -spacing - 2]  # central
        h_a = x[spacing + s + 1: -spacing + s - 1]  # after
        peak_candidate = np.logical_and(peak_candidate, np.logical_and(h_c > h_b, h_c > h_a))

    ind = np.argwhere(peak_candidate) + spacing  # correction for central
    ind = ind.reshape(ind.size)
    if limit is not None:
        ind = ind[x[ind] > limit]
    return ind


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    n = 1000
    m = 30
    t = np.linspace(0., 1, n)
    x = np.zeros(n)
    np.random.seed(0)
    phase = 2 * np.pi * np.random.random(m)
    for i in range(m):
        x += np.sin(phase[i] + 2 * np.pi * t * i)

    peaks = findpeaks(x, spacing=100, limit=4.)
    plt.plot(t, x)
    plt.plot(t[peaks], x[peaks], 'ro')
    plt.show()
