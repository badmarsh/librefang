import json
from pathlib import Path

def test_conformal_threshold_generation():
    """Verify that conformal threshold provides requested coverage guarantee"""
    threshold_file = Path("data/conformal_threshold.json")
    if not threshold_file.exists():
        # Try to run it if it doesn't exist
        import subprocess
        subprocess.run(["python3", "scripts/conformal_calibration.py"], check=True)
        
    assert threshold_file.exists()
    
    with open(threshold_file, "r") as f:
        data = json.load(f)
        
    assert "q_hat" in data
    assert data.get("alpha") == 0.10
    assert data.get("conformal_coverage_guarantee") == 0.90
    assert data.get("empirical_coverage", 0.0) >= 0.88
