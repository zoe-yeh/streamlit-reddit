import toml

output_file = ".streamlit/secrets.toml"
# output_file = "secrets.toml"

with open("streamlit-reddit-ebe13-firebase-adminsdk-h9zlm-e391adb04f.json") as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)