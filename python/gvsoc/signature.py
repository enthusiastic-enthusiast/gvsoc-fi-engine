#
# Copyright (C) 2026 GreenWaves Technologies, SAS, ETH Zurich and
#                    University of Bologna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Class-based port signatures for the gvrun2 systree.

A signature class describes a port's protocol/interface. The framework
compares master-side and slave-side signatures when bindings are flattened
and, if they don't match, asks the master signature to produce a bridge
component that is auto-inserted between the two ports.

Today the only axis the framework checks is the protocol (big-packet io_v2
vs beat-mode io_v2). The same mechanism is the natural extension point for
clock-domain crossings, voltage-domain crossings, address-width adapters,
etc. Subclasses add the checks; the binding machinery in systree_gvrun2.py
does not need to grow.
"""


class Signature:
    """Base class for class-based port signatures.

    Subclasses describe a particular protocol/interface. The framework asks
    the master-side signature whether it can be bound directly to the
    slave-side signature, and if not, asks it to produce a bridge component.
    """

    # Stable string tag used to interoperate with the legacy ``signature='...'``
    # string check. None means there is no legacy-string equivalent.
    tag = None

    def is_compatible(self, other):
        """Return True if a master with ``self`` can bind directly to a slave with ``other``."""
        return type(self) is type(other)

    def bridge_to(self, other, parent, name):
        """Return a bridge Component to place between master (``self``) and slave (``other``),
        or None if no bridge is needed.

        The default raises if signatures aren't compatible — subclasses that
        know how to bridge to a specific peer override and return a Component.
        ``parent`` is the component hosting the binding; the bridge should
        register itself as a child of ``parent`` (which the standard
        Component constructor already does).
        """
        if self.is_compatible(other):
            return None
        raise RuntimeError(
            f"Incompatible signatures and no bridge defined: "
            f"master={type(self).__name__} -> slave={type(other).__name__}")


class IoV2BigPacket(Signature):
    """io_v2 master/slave operating on whole-packet semantics.

    The slave may answer in any of the three v2 response forms; a big-packet
    master tolerates all of them per the v2 protocol contract."""

    tag = 'io_v2'


class IoV2Beat(Signature):
    """io_v2 master that wants its response normalised to one ``resp()`` per beat.

    The master receives one ``resp_meth`` call per beat with ``req->is_first``,
    ``is_last``, ``burst_id``, ``size``, ``data`` and ``status`` set per beat
    (the existing beat-form response contract of v2).
    """

    tag = 'io_v2'

    def __init__(self, beat_width):
        self.beat_width = beat_width

    def is_compatible(self, other):
        return isinstance(other, IoV2Beat) and other.beat_width == self.beat_width

    def bridge_to(self, other, parent, name):
        # Same-mode peer (IoV2Beat <-> IoV2Beat, same beat_width): no adapter.
        if self.is_compatible(other):
            return None
        # Mismatched mode (IoV2Beat master <-> IoV2BigPacket slave, or legacy
        # ``'io_v2'`` string slave that is by default big-packet): adapter
        # normalises the slave's response into a uniform per-beat stream.
        # The legacy string is the historic v2 default and matches IoV2BigPacket
        # semantically — the slave is free to answer in any of the three
        # response forms, including the sync DONE that beat-fidelity masters
        # cannot consume directly.
        if isinstance(other, IoV2BigPacket) or other == IoV2BigPacket.tag:
            from utils.io_v2_beat_adapter import IoV2BeatAdapter
            return IoV2BeatAdapter(parent, name, beat_width=self.beat_width)
        # IoV2Beat <-> IoV2Beat with differing widths is a SoC design error,
        # not a missing adapter.
        return super().bridge_to(other, parent, name)
