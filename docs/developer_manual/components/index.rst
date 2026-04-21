Components
==========

This section documents the GVSoC components that can be instantiated from
Python generators. Each page describes the generator class, its ports, and
the unit tests that exercise the component.

The pages are generated at doc build time from the registry in
``components_registry.py`` by walking ``GVSOC_MODULES``. Add an entry to that
file to include a new component.

.. toctree::
   :maxdepth: 1

   _generated/index
