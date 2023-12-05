
import ami.graph_nodes as gn
import amitypes
import numpy as np
from ami.flowchart.library.common import CtrlNode


# ##### utility functions #####
def remove_bkg(img, n1, n2):
    """
    Subtract a sized n1 top left and n2 bottom right square average intensity
    from the image.

    Parameters
    ----------
    img: np.ndarray
        Input image
    n1, n2: int
        Sizes of the top left and bottom right squares
    """
    img -= (img[:n1, :n1].mean() + img[-n2:, -n2:].mean())/2
    return img


def stats_from_moments(x, y=None):
    """
    Weigted mean, sigma, and skew.
    Use case is typically for quick stats on a gaussian-like
    distribution.

    Parameters
    ----------
    x: np.ndarray
        values
    y: np.ndarray
        weights
    """
    if y is None:
        y = np.ones_like(x)
    #y = np.abs(y)  # negative values in the baseline screw things up
    mean = np.sum(x*y) / np.sum(y)
    variance = np.sum((x-mean)**2*y) / y.sum()
    sigma = np.sqrt(variance)
    skew = np.sum((x-mean)**3*y) / sigma**3
    return mean, sigma, skew


def moment_2d(img, m, n):
    """
    Calculate the m, n moment of an image.

    Parameters
    ----------
    img : np.ndarray
        Input array image
    m, n: int
        moment order on i,j respectively
    """
    si, sj = img.shape
    ii = np.arange(si)
    jj = np.arange(sj)
    M_mn = np.dot(ii**m, np.dot(jj**n, img.T))
    return M_mn


def central_moment_2d(img, centroid, m, n):
    """
    Calculate the m, n central moment of an image.

    Parameters
    ----------
    img : np.ndarray
        Input array image
    centroid :
        Centroid coordinate (i,j)
    m, n: int
        Moment order on i,j respectively
    """
    ci, cj = centroid
    si, sj = img.shape
    ii = np.arange(si)
    jj = np.arange(sj)
    Mc_mn = np.dot((ii-ci)**m, np.dot((jj-cj)**n, img.T))
    return Mc_mn


def centroid_from_moments(m_00, m_10, m_01):
    centroid = (m_10/m_00, m_01/m_00)
    return centroid


def covariance_from_moments(centroid, m_00, mc_20, mc_11, mc_02):
    ci, cj = centroid
    cov = np.array([
        [mc_20/m_00-ci**2, mc_11/m_00-ci*cj],
        [mc_11/m_00-ci*cj, mc_02/m_00-cj**2]
    ])
    return cov


def image_stats(img):
    m00 = moment_2d(img, 0, 0)
    m10 = moment_2d(img, 1, 0)
    m01 = moment_2d(img, 0, 1)
    centroid = centroid_from_moments(m00, m10, m01)

    mc_20 = central_moment_2d(img, centroid, 2, 0)
    mc_11 = central_moment_2d(img, centroid, 1, 1)
    mc_02 = central_moment_2d(img, centroid, 0, 2)
    cov = covariance_from_moments(centroid, m00, mc_20, mc_11, mc_02)

    return centroid, cov


def image_stats_projection(img):
    centroid = 0
    sigma = 0
    return centroid, sigma


# ##########


class EventProcessor():

    def __init__(self):
        self.use_proj = False
        self.bkg_idx = (10, 10)  # index for background removal
        return

    def begin_run(self):
        pass

    def end_run(self):
        pass

    def begin_step(self, step):
        pass

    def end_step(self, step):
        pass

    def on_event(self, img, *args, **kwargs):
        use_proj = bool(self.use_proj)
        if self.bkg_idx != (0, 0):
            img = remove_bkg(img, self.bkg_idx[0], self.bkg_idx[1])

        if use_proj:
            i_idx = np.arange(img.shape[0])
            com_i, sig_i, skw_i = stats_from_moments(i_idx, y=img.sum(axis=1))

            j_idx = np.arange(img.shape[1])
            com_j, sig_j, skw_j = stats_from_moments(j_idx, y=img.sum(axis=0))
            fwhm_i, fwhm_j = (2.355*sig_i, 2.355*sig_j)
        else:
            com, cov = image_stats(img)
            fwhm_i = 0
            fwhm_j = 0
            com_i, com_j = com

        return com_i, com_j, fwhm_i, fwhm_j


class Centroid(CtrlNode):
    """
    Calculate the centroid of a given array.
    Two methods are available:
    1. Image moments: calculate moments on the full image directly
    2. Moment on projection along the horizontal and vertical directions

    For all method a background is subtracted. The background by default is the average of 10x10
    pixels at the upper left and lower right corner. Make sure these area do not contain signal.

    TO DO: gaussian fit method

    """

    nodeName = "Centroid"
    uiTemplate = [
        ('use_projection', 'check', {'checked': False}),
        ('bkg_n1', 'intSpin', {'value': 10, 'min': 0}),
        ('bkg_n2', 'intSpin', {'value': 10, 'min': 0}),
    ]

    def __init__(self, name):
        super().__init__(
            name,
            terminals={
                'img': {'io': 'in', 'removable': True, 'ttype': amitypes.array.Array2d, 'optional': False, 'group': None},
                'com_i': {'io': 'out', 'removable': True, 'ttype': float, 'optional': False, 'group': None},
                'com_j': {'io': 'out', 'removable': True, 'ttype': float, 'optional': False, 'group': None},
                'fwhm_i': {'io': 'out', 'removable': True, 'ttype': float, 'optional': False, 'group': None},
                'fwhm_j': {'io': 'out', 'removable': True, 'ttype': float, 'optional': False, 'group': None},
            }
        )

    def to_operation(self, **kwargs):
        proc = EventProcessor()
        proc.use_proj = self.values['use_projection']

        return gn.Map(name=self.name()+"_operation", **kwargs,
                      func=proc.on_event,
                      begin_run=proc.begin_run,
                      end_run=proc.end_run,
                      begin_step=proc.begin_step,
                      end_step=proc.end_step)
