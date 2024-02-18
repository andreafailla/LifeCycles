********
API docs
********

``lifecycles`` composes of several modules, each of which provides a set of functionalities for analyzing and visualizing the evolution of a group/set in time.
In this section all the functionalities of the library are described in detail.

.. note::
    All functions introduced below are available in the ``lifecycles`` namespace
    (except for the  ``LifeCycle`` class methods, which must be called on an instance of the class).
    This means that you can access them by importing the package and then calling the function, without importing the dedicated module.
    for example:
    ``lifecycles.viz.plot_set_flow`` can be accessed by calling ``lifecycles.plot_set_flow``.

.. warning:: The documentation is still under development. Some sections may be incomplete or missing.

----------------------
The LifeCycle class
----------------------

``lifecycle.classes`` provides the main class for storing and analyzing the longitudinal evolution of clusters.


.. toctree::
   :maxdepth: 1

   classes.rst

---------------
Flow Analytics
---------------
``lifecycles.algorithms`` provides a set of functions for quantifying the flow of elements across adjacent temporal clusters.

.. toctree::
   :maxdepth: 1

   flow_analytics.rst


----------------
Flow Validation
----------------
``lifecycles.validation`` provides a set of functions to extract statistically significant flows.

.. toctree::
   :maxdepth: 1

   validation.rst


-------------
Visualization
-------------

``lifecycles.viz`` provides a set of functions for visualizing the evolution of a group/set in time.

.. toctree::
   :maxdepth: 1

   visual_analytics.rst
