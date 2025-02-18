"""
Tests binenv's distributions file
"""

import yaml
import time
import os, sys

H = os.environ["HOME"]
# os.environ["PATH"] = ":".join([os.environ["HOME"], os.environ["PATH"]])
fn_distris = H + "/.config/binenv/distributions.yaml"


def checknonelf(b):
    d = H + "/.binenv/binaries/" + b
    if not os.path.exists(d):
        return f"missing {d}"
    for k in os.listdir(d):
        fn = d + "/" + k
        start = open(fn, "rb").read(40)
        if b"ELF" in start[:4]:
            return
        if b"#!/" in start[:3]:  # shebang, ok
            return
        return f'{k} head: `{start}`'
    return f"No files in {b}"


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
            uninst.append([k])
            continue

        e = checknonelf(k)
        if e:
            print(f"🟤 {k}: failed ELF check ({e})")
            nonelf.append([k, e])

    md = ["# Binenv Test Results"]
    md.append('- ' +os.popen("binenv version").read().strip())
    md.append('- ' +time.ctime())
    for n, failed in [("Uninstallable", uninst), ("Non ELF", nonelf)]:
        md.append(f"## {n} [{len(failed)} files]")
        for k in failed:
            md.append(f"- **{k[0]}**  ")
            if len(k) > 1:
                md.append(f"  {k[1]}")


    with open("binenv-tests.md", "w") as f:
        f.write("\n".join(md))


if __name__ == "__main__":
    main()
