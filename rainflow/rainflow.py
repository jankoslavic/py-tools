import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
import os

_file = 'rainflow'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
_rf = ctypes.cdll.LoadLibrary(_path)

def _sig2ext(sig, time_sig = None, clsn=-1):
    """Converts signal ``sig`` to turning  points used by ``rainflow``. The
    syntax is: ::

        (ntp, ext, exttime) = sig2ext(sig, clsn, [time_vals=None])

    where ``ntp`` is the number of turning points, ``ext`` is a turning-point
    signal and ``exttime`` are the corresponding time values.

    :param sig: signal as numpy array
    :param time_sig: time data of the signal, if `None` time is assumed as 0, 1, 2,...
    :param clsn: number of classes (pass -1 if not to be used, i.e., no divisions into classes)
    :return (ntp, ext, exttime):
    """
    sig = np.asarray(sig, dtype=float)
    sig = np.ascontiguousarray(sig)
    ext = np.ascontiguousarray(np.zeros_like(sig))
    exttime = np.ascontiguousarray(np.zeros_like(sig))
    try:
        __sig2ext = _rf.sig2ext
        __sig2ext.restype = ctypes.c_int
        if time_sig is None:
            __sig2ext.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                                 ctypes.c_voidp,#ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                                 ctypes.c_int,
                                 ctypes.c_long,
                                 ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                                 ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]
            ntp = __sig2ext(sig, None, len(sig), clsn,
                                ext, exttime)
        else:
            __sig2ext.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                                 ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                                 ctypes.c_int,
                                 ctypes.c_long,
                                 ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                                 ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]
            time_sig = np.asarray(time_sig, dtype=float)
            time_sig = np.ascontiguousarray(time_sig)
            ntp = __sig2ext(sig, time_sig, len(sig), clsn,

                           ext, exttime)
    except:
        raise Exception('sig2ext raised exception.')

    return (ntp, ext, exttime)

def _rainflow(ext, exttime=None):
    """Rainflow counting array_ext and array_t are results from sig2ext

    :param ext: is a turning-point signal and .
    :param exttime: are the corresponding time values
    :return: (cnr, rf)
           cnr: the number nonzero of rows in the rf matrix
           rf[:, 0] Cycles amplitude,
           rf[:, 1] Cycles mean value,
           rf[:, 2] Number of cycles (0.5 or 1.0),
           rf[:, 3] Begining time (when input includes exttime),
           rf[:, 4] Cycle period (when input includes exttime),
    """
    ext = np.ascontiguousarray(ext)
    try:
        _rf5 = _rf.rf5
        _rf5.restype = ctypes.c_int
        _rf3 = _rf.rf3
        _rf3.restype = ctypes.c_int

        if exttime is None:
            _rf3.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                             ctypes.c_int,
                             ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]
            array_out = np.ascontiguousarray(np.zeros((len(ext), 3)))
            cnr = _rf3(ext, len(ext), array_out)
        else:
            exttime = np.ascontiguousarray(exttime)
            _rf5.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                             ctypes.c_int,
                             ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                             ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]
            array_out = np.ascontiguousarray(np.zeros((len(ext), 5)))
            cnr = _rf5(ext, len(ext), exttime, array_out)
    except:
        raise Exception('_rainflow raised exception.')
    return cnr, array_out

def rainflow(sig, time_sig = None, clsn=-1):
    """Rainflow counting method

        (amplitude, mean, cycles) = rainflow(sig, time_sig, clsn) #if time_sig=None
        (amplitude, mean, cycles, start_time, period) = rainflow(sig, time_sig, clsn)

    :param sig: signal as numpy array
    :param time_sig: time data of the signal, if `None` time is assumed as 0, 1, 2,...
    :param clsn: number of classes (pass -1 if not to be used, i.e., no divisions into classes)
    :return:
           amplitude:  Cycles amplitude,
           mean:       Cycles mean value,
           cycles:     Number of cycles (0.5 or 1.0),
           start_time: Begining time (when input includes exttime),
           period:     Cycle period (when input includes exttime),
    """
    (ntp, ext, exttime) = _sig2ext(sig=sig, time_sig=time_sig, clsn=clsn)
    if time_sig is None:
        (_, rf) = _rainflow(ext[:ntp])
    else:
        (_, rf) = _rainflow(ext[:ntp], exttime[:ntp])

    up_to = np.where(rf[:,0]==0,)[0][0]

    amplitude = rf[:up_to,0]
    mean = rf[:up_to,1]
    cycles = rf[:up_to,2]
    if time_sig is None:
        return amplitude, mean, cycles
    else:
        start_time = rf[:up_to,3]
        period = rf[:up_to,4]
        return amplitude, mean, cycles, start_time, period

if __name__ == '__main__':
    sig = np.random.rand(10)
    import time

    tic = time.perf_counter()
    amp, mean, cyc = rainflow(sig)
    toc = time.perf_counter()
    print(1000*(toc-tic))
    print(amp)