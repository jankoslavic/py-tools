"""
Benchmark script to be used to evaluate the performance improvement of the MKL
Copyright (c) 2010, Didrik Pinte <dpinte@enthought.com>
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or other 
materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.

Source: https://dpinte.wordpress.com/2010/01/15/numpy-performance-improvement-with-the-mkl/
"""
import os
import sys
import timeit

import numpy as np


def test_eigenvalue():
    """
    Test eigen value computation of a matrix
    """
    i = 500
    data = np.random.random((i, i))
    result = np.linalg.eig(data)


def test_svd():
    """
    Test single value decomposition of a matrix
    """
    i = 1000
    data = np.random.random((i, i))
    result = np.linalg.svd(data)
    result = np.linalg.svd(data, full_matrices=False)


def test_inv():
    """
    Test matrix inversion
    """
    i = 1000
    data = np.random.random((i, i))
    result = np.linalg.inv(data)


def test_det():
    """
    Test the computation of the matrix determinant
    """
    i = 1000
    data = np.random.random((i, i))
    result = np.linalg.det(data)


def test_dot():
    """
    Test the dot product
    """
    i = 1000
    a = np.random.random((i, i))
    b = np.linalg.inv(a)
    result = np.dot(a, b) - np.eye(i)


# Test to start. The dict is the value I had with the MKL using EPD 6.0 and without MKL using EPD 5.1
tests = (test_eigenvalue,
         test_svd,
         test_inv,
         test_det,
         test_dot)

# Setting the following environment variable in the shell executing the script allows
# you limit the maximal number threads used for computation
THREADS_LIMIT_ENV = 'OMP_NUM_THREADS'


def start_benchmark():
    if THREADS_LIMIT_ENV in os.environ:
        print("Maximum number of threads used for computation is : %s" % os.environ[THREADS_LIMIT_ENV])
        print("-" * 80)
        print("Starting timing with numpy %s\nVersion: %s" % (np.__version__, sys.version))
        print("%20s : %10s - %5s / %5s" % ("Function", "Timing [ms]", "MKL", "No MKL"))

    for fun in tests:
        t = timeit.Timer(stmt="%s()" % fun.__name__, setup="from __main__ import %s" % fun.__name__)
        res = t.repeat(repeat=3, number=1)
        timing = 1000.0 * sum(res) / len(res)
        print("%20s : %7.1f ms" % (fun.__name__, timing))


if __name__ == '__main__':
    start_benchmark()
