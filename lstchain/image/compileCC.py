import numpy as np
import numba
from numba.pycc import CC

def compileCC():
    """
    Ahead of time compilation with numba.
    This will creates c shared library with with optimized functions.

    Functions pool: 
    
    -log_gaussian_CC

    Evaluate the log of a normal law

    Parameters
    ----------
    x: numpy.float32 3D numpy.ndarray
        Value at which the log gaussian is evaluated
    mean: numpy.float64 3D numpy.ndarray
        Central value of the normal distribution
    sigma: numpy.float64 3D numpy.ndarray
        Width of the normal distribution

    Returns
    -------
    log_pdf: numpy.float64 3D numpy.ndarray
        Log of the evaluation of the normal law at x
    """
    
    cc = CC('log_gaussian_CC')
    cc.verbose = True
    @cc.export('log_gaussian_CC', 'f8[:,:,:](f4[:,:,:],f8[:,:,:],f8[:,:,:])')
    def log_gaussian_CC(x,mean,sigma):
        log_pdf = np.empty(mean.shape)
        for i in range(mean.shape[0]):
            for j in range(mean.shape[1]):
                for k in range(mean.shape[2]):
                    log_pdf[i,j,k] = -(x[i,j,0] - mean[i,j,k])*(x[i,j,0] - mean[i,j,k])/2.0/sigma[i,j,k]/sigma[i,j,k] - np.log(np.sqrt(2*3.141592653589793)*sigma[i,j,k]);
        return log_pdf
    @cc.export('log_gaussian2_CC', 'f8[:,:](f4[:,:],f8[:,:],f8[:,:])')
    def log_gaussian2_CC(x,mean,sigma):
        log_pdf = np.empty(mean.shape)
        for i in range(mean.shape[0]):
            for j in range(mean.shape[1]):
                log_pdf[i,j] = -(x[i,j] - mean[i,j])*(x[i,j] - mean[i,j])/2.0/sigma[i,j]/sigma[i,j] - np.log(np.sqrt(2*3.141592653589793)*sigma[i,j]);
        return log_pdf
    cc.compile()
