import os, glob
import re

files = glob.glob("crates/librefang-api/tests/**/*.rs", recursive=True)
for f in files:
    with open(f, "r") as file:
        content = file.read()
    
    content = re.sub(r"(cfg\.api_key\s*=\s*[^;]+?\.to_string\(\));", r"\1.into();", content)
    content = re.sub(r"(cfg\.api_key\s*=\s*String::new\(\));", r"\1.into();", content)
    
    with open(f, "w") as file:
        file.write(content)
