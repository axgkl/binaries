import yaml
import requests
import os

# os.environ["PATH"] = ":".join([os.environ["HOME"], os.environ["PATH"]])
fn_distris = os.environ["HOME"] + "/.config/binenv/distributions.yaml"


def main():
    with open(fn_distris) as f:
        data = yaml.safe_load(f)
    uninst = []
    for k, spec in data["sources"].items():
        b = spec["install"].get("binaries")
        print("🟩 testing", k, b)
        if os.system("binenv install " + k):
            print("🟠 install failed", k)
            uninst.append(k)

        elif os.system(k + " --version"):
            print("🟥 failed", k)


if __name__ == "__main__":
    main()
