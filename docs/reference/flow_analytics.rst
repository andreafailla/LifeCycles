*************************
Flow Analytics
*************************

This module contains some

.. automodule:: lifecycles.algorithms


-------------
Analysis
-------------
``lifecycles`` provides a quick way to compute statistics related to group evolution.
The functions below are used to compute event facet scores as defined in the paper.

.. autosummary::
    :toctree: algorithms/

    lifecycles.algorithms.analyze_flow
    lifecycles.algorithms.analyze_all_flows


-------------
Measures
-------------
``lifecycles`` provides some measures to characterize the structural and attributive evolution of groups.
Apart from the newly introduced facet scores, the following measures are also provided:

.. autosummary::
    :toctree: algorithms/

    lifecycles.algorithms.contribution_factor
    lifecycles.algorithms.difference_factor
    lifecycles.algorithms.attribute_entropy_change
    lifecycles.algorithms.purity
    lifecycles.algorithms.event_typicality




