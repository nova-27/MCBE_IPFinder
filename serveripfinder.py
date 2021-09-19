import asyncio

import pyshark
from mcstats import mcstats
from mcstats.main import StatsNetworkError, StatsServerData
from pyshark.packet.layer import Layer
from pyshark.packet.packet import Packet


class ServerIPFinder:
    def __init__(self):
        self.destinations: dict[str, int] = {}

    def _packet_callback(self, packet: Packet):
        try:
            ip_layer: Layer = next(layer for layer in packet.layers if layer.layer_name == 'ip')
            udp_layer: Layer = next(layer for layer in packet.layers if layer.layer_name == 'udp')
        except StopIteration:
            return
        self.destinations[ip_layer.get_field('dst')] = int(udp_layer.get_field('dstport'))

    def get_destinations(
            self,
            interface,
            pyshark_display_filter='udp && ip.dst != 192.168.0.0/16',
            pyshark_timeout=10
    ):
        self.destinations = {}
        cap = pyshark.LiveCapture(interface, display_filter=pyshark_display_filter)
        try:
            cap.apply_on_packets(self._packet_callback, timeout=pyshark_timeout)
        except asyncio.exceptions.TimeoutError:
            pass
        return self.destinations

    def get_mc_servers(self, query_timeout=5) -> list[tuple[str, int, StatsServerData]]:
        if not self.destinations:
            return []
        mc_servers = []
        for ip, port in self.destinations.items():
            try:
                with mcstats(ip, port=port, timeout=query_timeout) as data:
                    mc_servers.append((ip, port, data))
            except StatsNetworkError:
                pass
        return mc_servers
