_="binenv installer
Understands:
- URL_BINENV_DISTRIS: Custom patches and adds for distributions.yaml
- BINENV_TOOLS: Tools to install, e.g.: 'go 1.15.6 node 14.15.4 btop' (with or w/o versions)
"
be="https://github.com/devops-works/binenv/releases/download/v0.19.11"
wget -q $be/binenv_linux_amd64
wget -q $be/checksums.txt
sha256sum --check --ignore-missing checksums.txt
mkdir -p "$HOME/.config/binenv"
mv binenv_linux_amd64 binenv
chmod +x binenv && ./binenv update && ./binenv install binenv && rm binenv && rm checksums.txt

ZESHELL=bash && if [[ -n $ZSH_NAME ]]; then ZESHELL=zsh; fi

# adding patches to distributions.yaml:
# When there is a NEW one, then there is no version info in the cache - but can be supplied by the user
type binenv 2>/dev/null || {
    echo -e '\nexport PATH=~/.binenv:$PATH' >>~/".${ZESHELL}rc"
    . ~/".${ZESHELL}rc"
}

test -z "${URL_BINENV_DISTRIS:-}" || wget -O - -q "$URL_BINENV_DISTRIS" |
    grep '^ ' >>"$HOME/.config/binenv/distributions.yaml"

test -z "$BINENV_TOOLS" && return 0

echo "Installing tools: $BINENV_TOOLS"

prev=""
for item in $BINENV_TOOLS x; do
    if [[ $item != *.* && $prev != *.* && -n $prev ]]; then
        echo "No version for tool: $prev"
        # no fail exit code for failed versions, need to do grep output:
        test "$(binenv versions "$prev" | grep "$prev" | cut -d : -f 2 | tr -d ' ')X" == "X" && {
            echo "No version in cache - tool unknown to binenv standard: $prev"
            binenv update "$prev" -f
        }
        binenv install "$prev"
    fi
    if [[ $item == *.* && $prev != *.* && -n $prev ]]; then
        binenv install "$prev" "$item"
    fi
    prev="$item"
done
