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
        start = open(fn, "rb").read(40)
        if b"ELF" in start[:4]:
            return
        if b"#!/" in start[:3]:  # shebang, ok
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
            e = f"🟤 {k}: failed ELF check ({e})"
            print(e)
            nonelf.append(e[2:])
            break

    md = ["# Binenv test results"]
    for n, l in [("Uninstallable", uninst), ("Non ELF", nonelf)]:
        md.append(f"## {n} [{len(l)} files]")
        for k in l:
            md.append(f"- {k}")

    with open("binenv-tests.md", "w") as f:
        f.write("\n".join(md))


if __name__ == "__main__":
    main()
