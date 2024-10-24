^^^^^^^^^^
LifeCycle
^^^^^^^^^^
.. currentmodule:: lifecycles

The ``LifeCycle`` class is the primary object for representing and analyzing time-aware clusters.
Here is a brief overview of the methods available for ``LifeCycle`` objects, structured in thematic groups.


------------------------
Partition-based Methods
------------------------

These methods are used to store and access temporally ordered partitions of the data.

.. autosummary::
    :toctree: classes/
    :nosignatures:

    LifeCycle.add_partition
    LifeCycle.add_partitions_from
    LifeCycle.get_partition_at

------------------------
Group-based Methods
------------------------

These methods are used to retrieve, filter, and analyze the individual clusters in the data.

.. autosummary::
    :toctree: classes/
    :nosignatures:

    LifeCycle.get_group
    LifeCycle.group_iterator
    LifeCycle.filter_on_group_size
    LifeCycle.group_flow
    LifeCycle.all_flows

------------------------
Element-based Methods
------------------------

These methods are used to retrieve the membership of individual items in the data (i.e., the groups they belong to).

.. autosummary::
    :toctree: classes/
    :nosignatures:

    LifeCycle.get_element_membership
    LifeCycle.get_all_element_memberships

------------------------
Attribute-based Methods
------------------------

These methods are used to store and access time-changing metadata assigned to the individual clusters.

.. autosummary::
    :toctree: classes/
    :nosignatures:

    LifeCycle.set_attributes
    LifeCycle.get_attributes


--------------------------
Other Convenience Methods
--------------------------

These methods are used to retrieve fundamental information about the data such as the universe set, and the list of time instants.

.. autosummary::
    :toctree: classes/
    :nosignatures:

    LifeCycle.groups_ids
    LifeCycle.temporal_ids
    LifeCycle.universe_set
    LifeCycle.slice




------------------------
IO Methods
------------------------

These methods are used to read and write ``LifeCycle`` objects to and from disk.

.. autosummary::
    :toctree: classes/
    :nosignatures:

    LifeCycle.to_dict
    LifeCycle.write_json
    LifeCycle.read_json


------------------------
Complete LifeCycle API
------------------------

.. note:: Object methods and functions are reported in alphabetical order.

.. autoclass:: LifeCycle
    :members:
    :undoc-members:
    :show-inheritance:






