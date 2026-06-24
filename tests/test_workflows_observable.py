import json
import tomllib
import glob
import pytest
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORKFLOWS = glob.glob(os.path.join(os.path.dirname(__file__), '../workflows/*.json')) + \
            glob.glob(os.path.join(os.path.dirname(__file__), '../workflows/*.toml'))

@pytest.mark.parametrize("filepath", WORKFLOWS)
def test_workflow_observability(filepath):
    logger.info(f"\\n--- Testing Workflow: {filepath} ---")
    
    if filepath.endswith('.json'):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
    else:
        with open(filepath, 'rb') as fp:
            data = tomllib.load(fp)
            
    steps = data.get('steps', [])
    if not steps:
        logger.warning(f"No steps found in {filepath}")
        return
        
    logger.info(f"Total Steps: {len(steps)}")
    
    # Map steps to check for invalid dependencies
    step_names = {s.get('name') for s in steps if 'name' in s}
    
    for i, step in enumerate(steps):
        name = step.get('name', f'unnamed_{i}')
        agent = step.get('agent', 'unknown_agent')
        mode = step.get('mode', 'sequential')
        depends_on = step.get('depends_on', [])
        
        logger.info(f"-> Step '{name}' [Agent: {agent}]")
        logger.info(f"   Mode: {mode}")
        
        if depends_on:
            logger.info(f"   Depends On: {depends_on}")
            for dep in depends_on:
                assert dep in step_names, f"Dependency {dep} not found in workflow {filepath}"
                
        # If conditional, log it
        if isinstance(mode, dict) and 'conditional' in mode:
            cond = mode['conditional'].get('condition', 'unknown')
            logger.info(f"   [!] Conditional trigger: {cond}")
            
        # Verify no legacy fields
        assert 'model' not in step, f"'model' found in {filepath} at step {name}"
        assert 'extra_body' not in step, f"'extra_body' found in {filepath} at step {name}"
        assert 'config' not in step, f"'config' found in {filepath} at step {name}"
        assert 'parallel' not in step, f"'parallel' found in {filepath} at step {name}"

    logger.info(f"--- Completed Observable Check for {filepath} ---")
