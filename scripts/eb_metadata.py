from easybuild.tools.options import set_up_configuration
from easybuild.framework.easyconfig.easyconfig import process_easyconfig
from pathlib import Path
import pandas as pd
import json

def homepage_link(text, url):
    if pd.notna(url) and url:
        return f"[{text}]({url})"
    return text

software = Path("/apps/USE/easybuild/release/2025.1/software/")
stack = []

options, cfg_settings = set_up_configuration(args=[])

# for eb in software.rglob("*.eb"):
#     print(eb)
    
#     try:
#         ecs = process_easyconfig(str(eb), validate = False)

#         for ecdict in ecs:
#             ec = ecdict["ec"]

#             package = {
#                 "name": ec["name"],
#                 "version": ec["version"],
#                 "homepage": ec["homepage"],
#                 "description": ec["description"],
#                 "moduleclass": ec["moduleclass"],
#             }

#             stack.append(package)
        
#     except Exception as excpt:
#         print(f"Failed: {eb}: {excpt}")


# with open("stack.json", "w") as fp:
#     json.dump(stack, fp, indent=2, default=str)

stack = pd.read_json("stack.json")

df = pd.DataFrame(stack)

# Create Markdown hyperlinks
df["software"] = df.apply(
    lambda row: homepage_link(row["name"], row["homepage"]),
    axis=1,
)

# Clean descriptions
df["description"] = (
    df["description"]
      .fillna("")
      .str.replace(r"\s+", " ", regex=True)
      .str.strip()
)
#Reorder columns
df = df[
    [
        "software",
        "version",
        "moduleclass",
        "description",
    ]
]

# Sort alphabetically
df = df.sort_values(["software", "version"])

# Write Markdown
with open("stack.md", "w") as f:
    f.write(df.to_markdown(index=False))

# Keep JSON too
#df.to_json("stack.json", orient="records", indent=2)
