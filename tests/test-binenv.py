import yaml
import requests
import os

# os.environ["PATH"] = ":".join([os.environ["HOME"], os.environ["PATH"]])
fn_distris = os.environ["HOME"] + "/.config/binenv/distributions.yaml"


def main():
    with open(fn_distris) as f:
        data = yaml.safe_load(f)
    for k, spec in data["sources"].items():
        b = spec["install"].get("binaries")
        print("🟩 testing", k, b)
        os.system("binenv install " + k)
        if os.system(k):
            print("🟥 failed", k)


if __name__ == "__main__":
    main()
