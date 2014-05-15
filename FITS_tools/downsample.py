import numpy as np

def downsample_axis(myarr, factor, axis, estimator=np.nanmean, truncate=False):
    """
    Downsample an ND array by averaging over *factor* pixels along an axis.
    Crops right side if the shape is not a multiple of factor.

    This code is pure np and should be fast.

    keywords:
        estimator - default to mean.  You can downsample by summing or
            something else if you want a different estimator
            (e.g., downsampling error: you want to sum & divide by sqrt(n))
    """
    # size of the dimension of interest
    xs = myarr.shape[axis]
    
    if xs % int(factor) != 0:
        if truncate:
            view = [slice(None) for ii in range(myarr.ndim)]
            view[axis] = slice(None,xs-(xs % int(factor)))
            crarr = myarr[view]
        else:
            newshape = list(myarr.shape)
            newshape[axis] = (factor - xs % int(factor))
            extension = np.empty(newshape) * np.nan
            crarr = np.concatenate((myarr,extension), axis=axis)
    else:
        crarr = myarr

    def makeslice(startpoint,axis=axis,step=factor):
        # make empty slices
        view = [slice(None) for ii in range(myarr.ndim)]
        # then fill the appropriate slice
        view[axis] = slice(startpoint,None,step)
        return view

    # The extra braces here are crucial: We're adding an extra dimension so we
    # can average across it!
    stacked_array = np.concatenate([[crarr[makeslice(ii)]] for ii in range(factor)])

    dsarr = estimator(stacked_array, axis=0)
    return dsarr
