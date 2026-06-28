# Dezolator Science Lab

The Dezolator Science Lab provides cutting-edge computational social science simulations to model the spread of disinformation and the effects of interventions. Designed explicitly for AI agents, it exposes a CLI and programmatic API.

## Core Capabilities

1. **Synthetic Topology Generation**: 
   - `scale-free` (Barabási-Albert): Mimics Twitter follower networks where a few influencers have massive reach.
   - `small-world` (Watts-Strogatz): Mimics Facebook friend networks with tight clusters and short paths.
   - `polarized`: Generates two distinct echo-chambers with minimal interconnectivity, highly applicable for modern political disinformation.

2. **Complex Contagion Modeling**:
   - `linear-threshold`: Nodes adopt a narrative only when peer pressure reaches a critical mass. Disinformation is often a complex contagion, requiring multiple exposures to stick.
   - `sir`: Simple epidemiological viral spread, useful for purely algorithmic virality like botnets.

## AI Agent Use-Cases

- **Vulnerability Projections (Overseer)**: The `dezolator-overseer` can simulate a detected narrative cluster over a `polarized` topology using a `linear-threshold` model to project whether the narrative will escape its initial echo chamber and become apocalyptic.
- **Inoculation / Pre-bunking (Compliance/Strategist)**: Run A/B simulations. Run a baseline spread, then re-run reducing the `initial_fraction` of susceptible nodes (representing a successful pre-bunking campaign) to measure the reduction in `final_infected_percentage`.
- **Algorithmic De-amplification**: Modify network edges or use the SIR model with lower `beta` to measure the impact of shadow-banning superspreader nodes.

## Usage

```bash
# Simulate a highly polarized echo chamber spreading a complex contagion
python main.py --topology polarized --model linear-threshold --threshold 0.25 --nodes 2000

# Simulate a botnet amplifying a simple viral claim
python main.py --topology scale-free --model sir --beta 0.4 --gamma 0.05
```