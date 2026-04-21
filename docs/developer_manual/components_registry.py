# Registry of GVSoC components to include in the generated documentation.
#
# Each entry generates one page under components/_generated/<module>.<class>.rst.
# The generator resolves `module` via the paths listed in GVSOC_MODULES (the
# same env var the build system uses), so any import path that works at
# simulation time works here.
#
# Fields:
#   module     — Python import path of the generator file
#   class      — generator class name inside that module
#   title      — section title to render at the top of the page
#   tests_dirs — list of paths (relative to the repo root) whose testset.cfg
#                files are scraped for a "Tests" table. Optional; omit or set
#                to an empty list when a component has no dedicated tests.

COMPONENTS = [
    {
        'module':     'interco.router_v2',
        'class':      'Router',
        'title':      'Router (v2)',
        'tests_dirs': [
            'gvsoc/core/tests/interco/router_untimed',
            'gvsoc/core/tests/interco/router_bandwidth',
            'gvsoc/core/tests/interco/router_backpressure',
            'gvsoc/core/tests/interco/router_beat',
        ],
    },
]
