import argparse
import json
import logging
from network_topology import TopologyGenerator
from diffusion_engine import DiffusionEngine

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def run_simulation(args):
    generator = TopologyGenerator(size=args.nodes)
    
    # Generate Topology
    if args.topology == "scale-free":
        graph = generator.generate_scale_free(m=3)
    elif args.topology == "small-world":
        graph = generator.generate_small_world(k=6, p=0.1)
    elif args.topology == "polarized":
        graph = generator.generate_polarized_echo_chamber(m=3, interconnectivity=0.05)
    else:
        raise ValueError(f"Unknown topology: {args.topology}")
        
    engine = DiffusionEngine(graph)
    
    # Run Simulation
    if args.model == "sir":
        history = engine.simulate_sir(
            initial_infected_fraction=args.initial_fraction,
            beta=args.beta,
            gamma=args.gamma,
            max_steps=args.steps
        )
    elif args.model == "linear-threshold":
        history = engine.simulate_linear_threshold(
            initial_infected_fraction=args.initial_fraction,
            threshold=args.threshold,
            max_steps=args.steps
        )
    else:
        raise ValueError(f"Unknown contagion model: {args.model}")
        
    result = {
        "topology": args.topology,
        "nodes": args.nodes,
        "model": args.model,
        "history": history,
        "final_infected_percentage": (history[-1]["infected"] / args.nodes) * 100
    }
    
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dezolator Science Lab: Disinformation Diffusion Simulator")
    parser.add_argument("--nodes", type=int, default=1000, help="Number of nodes in the synthetic network")
    parser.add_argument("--topology", type=str, choices=["scale-free", "small-world", "polarized"], default="polarized", help="Network topology structure")
    parser.add_argument("--model", type=str, choices=["sir", "linear-threshold"], default="linear-threshold", help="Diffusion model algorithm")
    parser.add_argument("--initial-fraction", type=float, default=0.05, help="Initial fraction of nodes exposed to the disinformation")
    parser.add_argument("--beta", type=float, default=0.3, help="Infection probability (SIR model only)")
    parser.add_argument("--gamma", type=float, default=0.1, help="Recovery/Debunking probability (SIR model only)")
    parser.add_argument("--threshold", type=float, default=0.3, help="Threshold fraction for complex contagion (Linear Threshold only)")
    parser.add_argument("--steps", type=int, default=50, help="Maximum number of simulation steps")
    
    args = parser.parse_args()
    run_simulation(args)
