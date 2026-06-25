import networkx as nx
import logging

logger = logging.getLogger(__name__)

class TopologyGenerator:
    """
    Generates synthetic social network topologies for computational science simulations.
    Supports cutting-edge configurations that closely mimic real-world disinformation channels.
    """
    def __init__(self, size: int = 1000):
        self.size = size
        
    def generate_scale_free(self, m: int = 3) -> nx.Graph:
        """
        Barabási-Albert model: simulates power-law degree distributions
        found in follower-following networks (e.g., Twitter, Telegram channels).
        """
        logger.info(f"Generating scale-free (Barabási-Albert) network with {self.size} nodes (m={m})")
        return nx.barabasi_albert_graph(self.size, m)

    def generate_small_world(self, k: int = 6, p: float = 0.1) -> nx.Graph:
        """
        Watts-Strogatz model: captures high clustering and short path lengths.
        Excellent for modeling tight-knit echo chambers.
        """
        logger.info(f"Generating small-world (Watts-Strogatz) network with {self.size} nodes (k={k}, p={p})")
        return nx.watts_strogatz_graph(self.size, k, p)
        
    def generate_polarized_echo_chamber(self, m: int = 3, interconnectivity: float = 0.05) -> nx.Graph:
        """
        Generates two scale-free communities with minimal cross-edges,
        perfectly simulating polarized political landscapes.
        """
        logger.info(f"Generating polarized echo chamber network with size {self.size}")
        half = self.size // 2
        g1 = nx.barabasi_albert_graph(half, m)
        g2 = nx.barabasi_albert_graph(self.size - half, m)
        
        # Relabel nodes in g2 to ensure disjoint sets
        mapping = {n: n + half for n in g2.nodes()}
        g2 = nx.relabel_nodes(g2, mapping)
        
        G = nx.compose(g1, g2)
        
        # Add random weak ties to represent low interconnectivity
        num_ties = int(half * interconnectivity)
        import random
        for _ in range(num_ties):
            u = random.choice(list(g1.nodes()))
            v = random.choice(list(g2.nodes()))
            G.add_edge(u, v)
            
        return G
