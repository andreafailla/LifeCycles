********
API docs
********

``lifecycles`` composes of several modules, each of which provides a set of functionalities for analyzing and visualizing the evolution of groups in time.
This section points to pages that describe the functionalities of each module.


.. warning:: The documentation is still under development. Some sections may be incomplete or missing.

----------------------
Modules
----------------------

The library is composed of the following five modules. ``classes`` provides the main class for storing and analyzing the data.
``algorithms`` provides a set of functions for analyzing the evolution of a group in time as well as the events that may occur.
``validation`` provides a set of functions to extract statistically significant flows.
``viz`` provides visual analytics functions.
Finally, ``utils`` provides a set of utility functions for handling the data.

.. note::
    All functions introduced in the pages below are available in the ``lifecycles`` namespace
    (except for the  ``LifeCycle`` class methods, which must be called on an instance of the class).
    This means that you can access them by importing the package and then calling the function, without importing the dedicated module.
    for example:
    ``lifecycles.viz.plot_flow`` can be accessed by calling ``lifecycles.plot_flow``.



.. toctree::
   :maxdepth: 2

   classes.rst
   event_analytics.rst

.. toctree::
   :maxdepth: 1

   validation.rst
   visual_analytics.rst
   utils.rst
