import networkx as nx
import random
import logging

logger = logging.getLogger(__name__)

class DiffusionEngine:
    """
    Simulation engine for tracking the spread of disinformation claims
    across a network topology using complex contagion algorithms.
    """
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = list(graph.nodes())
        
    def simulate_sir(self, initial_infected_fraction: float = 0.01, beta: float = 0.3, gamma: float = 0.1, max_steps: int = 50):
        """
        Susceptible-Infected-Recovered model.
        In this context:
        - Susceptible: User has not seen the claim.
        - Infected: User believes/shares the claim.
        - Recovered: User debunked it or lost interest.
        """
        logger.info(f"Starting SIR simulation: beta={beta}, gamma={gamma}, initial={initial_infected_fraction}")
        
        # States: 0=S, 1=I, 2=R
        state = {n: 0 for n in self.nodes}
        num_initial = max(1, int(len(self.nodes) * initial_infected_fraction))
        initial_infected = random.sample(self.nodes, num_initial)
        for n in initial_infected:
            state[n] = 1
            
        history = []
        
        for step in range(max_steps):
            new_state = state.copy()
            S_count = I_count = R_count = 0
            
            for n in self.nodes:
                if state[n] == 1:
                    # Try to infect neighbors
                    for neighbor in self.graph.neighbors(n):
                        if state[neighbor] == 0 and random.random() < beta:
                            new_state[neighbor] = 1
                    
                    # Try to recover
                    if random.random() < gamma:
                        new_state[n] = 2
                        
            state = new_state
            
            for v in state.values():
                if v == 0: S_count += 1
                elif v == 1: I_count += 1
                elif v == 2: R_count += 1
                
            history.append({
                "step": step,
                "susceptible": S_count,
                "infected": I_count,
                "recovered": R_count
            })
            
            if I_count == 0:
                break # Epidemic died out
                
        return history

    def simulate_linear_threshold(self, initial_infected_fraction: float = 0.05, threshold: float = 0.3, max_steps: int = 20):
        """
        Complex contagion model modeling peer pressure / echo chamber effects.
        A node adopts the disinformation only if the fraction of infected neighbors exceeds a threshold.
        """
        logger.info(f"Starting Linear Threshold simulation: threshold={threshold}")
        state = {n: 0 for n in self.nodes}
        num_initial = max(1, int(len(self.nodes) * initial_infected_fraction))
        initial_infected = random.sample(self.nodes, num_initial)
        for n in initial_infected:
            state[n] = 1
            
        history = []
        
        for step in range(max_steps):
            new_state = state.copy()
            S_count = I_count = 0
            changed = False
            
            for n in self.nodes:
                if state[n] == 0:
                    neighbors = list(self.graph.neighbors(n))
                    if len(neighbors) > 0:
                        infected_neighbors = sum(1 for neighbor in neighbors if state[neighbor] == 1)
                        if (infected_neighbors / len(neighbors)) >= threshold:
                            new_state[n] = 1
                            changed = True
                            
            state = new_state
            for v in state.values():
                if v == 0: S_count += 1
                elif v == 1: I_count += 1
                
            history.append({
                "step": step,
                "susceptible": S_count,
                "infected": I_count
            })
            
            if not changed:
                break
                
        return history
