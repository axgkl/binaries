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
        return f"{k} head: `{start}`"
    return f"No files in {b}"


def main():
    with open(fn_distris) as f:
        data = yaml.safe_load(f)
    uninst = []
    nonelf = []
    works = []
    for k, spec in data["sources"].items():
        b = spec["install"].get("binaries")
        url = spec.get("url", "no url")
        desc = spec.get("description", "no descr")
        print("🟩 testing", k, b, file=sys.stderr)

        if os.system("binenv install " + k):
            print(f"🟠 {k} install failed")
            uninst.append([k, url, desc])
            continue

        e = checknonelf(k)
        if e:
            print(f"🟤 {k}: failed ELF check ({e})")
            nonelf.append([k, url, [desc, e]])
        works.append([k, url, desc])

    md = ["# Binenv Test Results"]
    add = md.append
    add("- " + os.popen("binenv version").read().strip())
    add("- " + time.ctime())
    for title, spec in [
        ("Uninstallable", uninst),
        ("Non ELF", nonelf),
        ("Working", works),
    ]:
        add("")
        add(f"## {title} <small>[{len(spec)} files]</small>")
        for i in spec:
            k, url, d = i
            add(f"- [**{k}**]({url})")
            add("```")
            if isinstance(d, list):
                add(d[0].strip().replace("```", ""))
                add(f"🟥 Error: {d[1]}")
            add("```")
            add("")

    with open("binenv-tests.md", "w") as f:
        f.write("\n".join(md))


if __name__ == "__main__":
    main()
