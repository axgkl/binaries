wget -q https://github.com/devops-works/binenv/releases/download/v0.19.11/binenv_linux_amd64
wget -q https://github.com/devops-works/binenv/releases/download/v0.19.11/checksums.txt
sha256sum --check --ignore-missing checksums.txt
mv binenv_linux_amd64 binenv
chmod +x binenv
./binenv update
./binenv install binenv
rm binenv
rm checksums.txt
if [[ -n $BASH ]]; then ZESHELL=bash; fi
if [[ -n $ZSH_NAME ]]; then ZESHELL=zsh; fi
test -z "${URL_BINENV_DISTRIS:-}" || wget -O - -q "$URL_BINENV_DISTRIS" | grep '^ ' >>$HOME/.config/binenv/distributions.yaml
type binenv 2>/dev/null || {
    echo -e '\nexport PATH=~/.binenv:$PATH' >>~/".${ZESHELL}rc"
    . ~/".${ZESHELL}rc"
}
test -z "${BINENV_TOOLS:-}" || eval "binenv install $BINENV_TOOLS"

#echo "source <(binenv completion ${ZESHELL})" >>~/".${ZESHELL}rc"
