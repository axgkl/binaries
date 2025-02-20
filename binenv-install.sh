wget -q https://github.com/devops-works/binenv/releases/download/v0.19.11/binenv_linux_amd64
wget -q https://github.com/devops-works/binenv/releases/download/v0.19.11/checksums.txt
sha256sum --check --ignore-missing checksums.txt
mkdir -p "$HOME/.config/binenv"
mv binenv_linux_amd64 binenv
chmod +x binenv
./binenv update
./binenv install binenv
rm binenv
rm checksums.txt
if [[ -n $BASH ]]; then ZESHELL=bash; fi
if [[ -n $ZSH_NAME ]]; then ZESHELL=zsh; fi
# adding patches to distributions.yaml:
# When there is a NEW one, then there is no version info in the cache - but can be supplied by the user
test -z "${URL_BINENV_DISTRIS:-}" || wget -O - -q "$URL_BINENV_DISTRIS" | grep '^ ' >>$HOME/.config/binenv/distributions.yaml
type binenv 2>/dev/null || {
    echo -e '\nexport PATH=~/.binenv:$PATH' >>~/".${ZESHELL}rc"
    . ~/".${ZESHELL}rc"
}
set -x
if [[ -n "$BINENV_TOOLS" ]]; then
    prev=""
    for item in $BINENV_TOOLS x; do
        if [[ $item != *.* && $prev != *.* && -n $prev ]]; then
            echo "No version for tool: $prev"
            # no fail exit code for failed versions, need to do grep output:
            test "$(binenv versions "$prev" | grep "$prev" | cut -d : -f 2 | tr -d ' ')X" == "X" && {
                echo "No version in cache - tool unknown to binenv standard: $prev"
                binenv update -f "$prev"
            }
        fi
        prev="$item"
    done

    set +x
    eval "binenv install $BINENV_TOOLS"
fi
echo "done tools"
