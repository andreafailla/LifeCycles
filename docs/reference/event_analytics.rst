*************************
Event Analytics
*************************

This module contains some

.. automodule:: lifecycles.algorithms


----------------
Events
----------------
``lifecycles`` provides a quick way to compute statistics related to group evolution.
The functions below are used to compute event facet scores as defined in the paper.

.. automodule:: lifecycles.algorithms

.. autosummary::
    :toctree: algorithms/event_analysis
    :nosignatures:

    lifecycles.algorithms.analyze_all_flows
    lifecycles.algorithms.analyze_flow
    lifecycles.algorithms.event
    lifecycles.algorithms.events_all
    lifecycles.algorithms.event_weights
    lifecycles.algorithms.facets

The module also provides some classical approaches to measure group evolution:

.. autosummary::
    :toctree: algorithms/event_analysis
    :nosignatures:

    lifecycles.algorithms.events_asur
    lifecycles.algorithms.event_graph_greene

-------------
Measures
-------------
``lifecycles`` provides some measures to characterize the structural and semantic evolution of groups.

.. autosummary::
    :toctree: algorithms/
    :nosignatures:

    lifecycles.algorithms.facet_unicity
    lifecycles.algorithms.facet_identity
    lifecycles.algorithms.facet_outflow
    lifecycles.algorithms.facet_metadata
    lifecycles.algorithms.purity
    lifecycles.algorithms.event_typicality
    lifecycles.algorithms.stability







