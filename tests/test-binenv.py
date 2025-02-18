import yaml
import requests
import os, sys

H = os.environ["HOME"]
# os.environ["PATH"] = ":".join([os.environ["HOME"], os.environ["PATH"]])
fn_distris = H + "/.config/binenv/distributions.yaml"


def checknonelf(k):
    d = H + "/.binenv/binaries/" + k
    if not os.path.exists(d):
        return f"missing {d}"
    for k in os.listdir(d):
        if not b"ELF" in open(d + "/" + k, "rb").read(4):
            return str(open(d + "/" + k, "rb").read(20))
        return
    return "no files"


def main():
    with open(fn_distris) as f:
        data = yaml.safe_load(f)
    uninst = []
    nonelf = []
    i = 0
    for k, spec in data["sources"].items():
        i += 1
        if i > 10:
            break
        b = spec["install"].get("binaries")
        print("🟩 testing", k, b, file=sys.stderr)

        if os.system("binenv install " + k):
            print(f"🟠 {k} install failed")
            uninst.append(k)
            continue
        e = checknonelf(k)
        if e:
            print(f"🟤 {k}: failed ELF check", b)
            nonelf.append(k)

    print("uninstallable", uninst, file=sys.stderr)
    print()
    print("non ELF", nonelf, file=sys.stderr)


if __name__ == "__main__":
    main()
