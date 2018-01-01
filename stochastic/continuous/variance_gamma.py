"""Variance gamma process."""
import numpy as np

from stochastic.base import Continuous


class VarianceGammaProcess(Continuous):
    r"""Variance Gamma process.

    A variance gamma process has independent increments which follow the
    variance-gamma distribution. It can be represented as a Brownian motion
    with drift subordinated by a Gamma process:

    .. math::

        \theta \Gamma(t; 1, \nu) + \sigma W(\Gamma(t; 1, \nu))

    :param float t: the right hand endpoint of the time interval :math:`[0,t]`
        for the process
    :param float drift: the drift parameter of the Brownian motion,
        or :math:`\theta` above
    :param float variance: the variance parameter of the Gamma subordinator,
        or :math:`\nu` above
    :param float scale: the scale parameter of the Brownian motion,
        or :math:`\sigma` above
    """

    def __init__(self, t=1, drift=0, variance=1, scale=1):
        super().__init__(t)
        self.drift = drift
        self.variance = variance
        self.scale = scale

    @property
    def drift(self):
        """Drift parameter."""
        return self._drift

    @drift.setter
    def drift(self, value):
        self._check_number(value, "Drift")
        self._drift = value

    @property
    def variance(self):
        """Variance parameter."""
        return self._variance

    @variance.setter
    def variance(self, value):
        self._check_positive_number(value, "Variance")
        self._variance = value

    @property
    def scale(self):
        """Scale parameter."""
        return self._scale

    @scale.setter
    def scale(self, value):
        self._check_positive_number(value, "Scale")
        self._scale = value

    def _sample_variance_gamma_process(self, n, zero=True):
        """Generate a realization of a variance gamma process."""
        self._check_increments(n)
        self._check_zero(zero)

        delta_t = 1.0 * self.t / n
        shape = delta_t / self.variance
        scale = self.variance

        gammas = np.random.gamma(shape=shape, scale=scale, size=n)
        gn = np.random.normal(size=n)

        increments = self.drift * gammas + self.scale * np.sqrt(gammas) * gn

        samples = np.cumsum(increments)

        if zero:
            return np.concatenate(([0], samples))
        else:
            return samples

    def sample(self, n, zero=True):
        """Generate a realization of a variance gamma process.

        :param int n: the number of increments to generate
        :param bool zero: if True, include :math:`t=0`
        """
        return self._sample_variance_gamma_process(n, zero)