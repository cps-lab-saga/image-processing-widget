from pathlib import Path

p = Path.cwd() / "plugins"

for f in p.glob("*.py"):
    info_p = p / (f.stem + ".image-processing-plugin")
    name = f.stem.replace("_", " ").title()
    version = "0.1"
    author = "Wen Liang Yeoh"

    contents = f"""[Core]
Name = {name}
Module = {f.stem}

[Documentation]
Author = Wen Liang Yeoh
Version = {version}
Description = {name}
"""
    with open(info_p, "w") as info_f:
        info_f.write(contents)
