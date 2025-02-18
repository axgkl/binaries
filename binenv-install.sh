wget -q https://github.com/devops-works/binenv/releases/download/v0.19.11/binenv_linux_amd64
mv binenv_linux_amd64 binenv
chmod +x binenv
./binenv update
./binenv install binenv
rm binenv
if [[ -n $BASH ]]; then ZESHELL=bash; fi
if [[ -n $ZSH_NAME ]]; then ZESHELL=zsh; fi
echo -e '\nexport PATH=~/.binenv:$PATH' >>~/".${ZESHELL}rc"
echo "source <(binenv completion ${ZESHELL})" >>~/".${ZESHELL}rc"
exec "$SHELL"
