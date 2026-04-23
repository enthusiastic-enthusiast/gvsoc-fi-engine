Components
==========

This section documents the GVSoC components that can be instantiated from
Python generators. Each page describes the generator class, its ports, and
the unit tests that exercise the component.

The pages are generated at doc build time by walking ``GVSOC_MODULES`` and
picking up every generator class that declares a ``__gvsoc_doc__`` class
attribute. Add such an attribute to a ``gvsoc.systree.Component`` subclass
to include it here.

.. toctree::
   :maxdepth: 1

   _generated/index
