import tomllib
with open("agents/predictor-hand/agent.toml", "rb") as f:
    try:
        data = tomllib.load(f)
        print("OK")
    except Exception as e:
        print("Error:", e)
