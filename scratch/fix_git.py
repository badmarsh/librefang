import re
with open("agents/coherence-checker/agent.toml", "r") as f:
    text = f.read()

text = re.sub(r"<<<<<<< HEAD\n.*?\n=======\n", "", text, flags=re.DOTALL)
text = re.sub(r">>>>>>> [^\n]+\n", "", text)

with open("agents/coherence-checker/agent.toml", "w") as f:
    f.write(text)
