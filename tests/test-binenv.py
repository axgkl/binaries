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
        fn = d + "/" + k
        start = open(fn, "rb").read(4)
        if b"ELF" in start:
            return
        if b"#!/" in start:  # shebang, ok
            return
        return start
    return f"no files in {d}"


def main():
    with open(fn_distris) as f:
        data = yaml.safe_load(f)
    uninst = []
    nonelf = []
    for k, spec in data["sources"].items():
        b = spec["install"].get("binaries")
        print("🟩 testing", k, b, file=sys.stderr)

        if os.system("binenv install " + k):
            print(f"🟠 {k} install failed")
            uninst.append(k)
            continue

        e = checknonelf(k)
        if e:
            print(f"🟤 {k}: failed ELF check ({e})")
            nonelf.append(k)

    print("uninstallable", uninst, file=sys.stderr)
    print()
    print("non ELF", nonelf, file=sys.stderr)


if __name__ == "__main__":
    main()
