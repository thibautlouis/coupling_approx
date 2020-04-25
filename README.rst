**************************
Toeplitz Approximation
**************************

We provide codes to check the validity of the Toeplitz Approximation for the coupling kernels involved in power spectra and covariance matrices computation.

Requirements
============

* pspy : python library for power spectrum estimation (https://github.com/simonsobs/pspy)


Pipeline flow chart
===================

The relevant parameters of the code are in the : ``global.dict``

The first step of the pipeline is generating a simulation of the CMB sky in CAR pixellisation

.. code:: shell

    python generate_sim.py global.dict

then we can generate the baseline window function

.. code:: shell

    python generate_window.py global.dict

The next step is to compute power spectra with exact mode coupling computation and the approximated one. In the global_dict, we have specified the baseline parameters to be

``l_exact_array = [None, 800]``
``l_band_array  = [None, 2000]``
``l_toep_array  = [None, 2500]``

When the parameters are set to None it corresponds to the exact computation.

.. code:: shell

    python compute_spectra.py.py global.dict
    
Note that this step will be long (that's the point of the study!) since we compute the coupling exactly up to l=10000.

You can plot spectra and residuals with

.. code:: shell

    python plot_spectra.py global.dict

