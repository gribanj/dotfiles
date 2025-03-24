sudo apt-get install libssl-dev pkg-config -y
sudo apt-get update -y
sudo apt-get install cmake -y
sudo apt-get install fzf -y
sudo apt-get install stow -y
sudo apt install tmux -y

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

cargo install eza

cd ~ && git clone git@github.com:nushell/nu_scripts.git

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# for Homebrew

==> Next steps:

- Run these commands in your terminal to add Homebrew to your PATH:
  echo >> /home/yuriyg/.bashrc
  echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/yuriyg/.bashrc
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
- Install Homebrew's dependencies if you have sudo access:
  sudo apt-get install build-essential
  For more information, see:
  https://docs.brew.sh/Homebrew-on-Linux
- We recommend that you install GCC:
  brew install gcc
- Run brew help to get started
- Further documentation:
  https://docs.brew.sh

brew install nushell

brew install jesseduffield/lazydocker/lazydocker

brew install eza

cargo install zoxide

zoxide init nu | save ~/.zoxide.nu

in nushell run:
cargo install atuin
mkdir ~/.local/share/atuin
atuin init nu | save ~/.local/share/atuin/init.nu

# test: atuin search keyword

in nushell run:
brew install carapace
mkdir ~/.cache/carapace
carapace setup nushell | save ~/.cache/carapace/init.nu

in nushell run:
cargo install nu_plugin_gstat
plugin add ~/.cargo/bin/nu_plugin_gstat
plugin list

in nushell run:
cargo install starship
mkdir ~/.cache/starship
starship init nu | save ~/.cache/starship/init.nu

eval "$(starship init bash)"

# https://thevaluable.dev/fzf-shell-integration/

in nushell run:
sudo apt-get install fzf -y
mkdir ~/.config/fzf
fzf init nu | save ~/.config/fzf/init.nu

in nushell run:
cargo install nu_plugin_query
plugin add ~/.cargo/bin/nu_plugin_query

cargo install aichat
https://github.com/sigoden/aichat?tab=readme-ov-file

####################################

mv ~/.config/nushell/config.nu ~/.config/nushell/config.nu.bak
mv ~/.config/nushell/env.nu ~/.config/nushell/env.nu.bak
mv ~/.config/nushell/plugin.msgpackz ~/.config/nushell/plugin.msgpackz.bak

mv ~/.bash_aliases ~/.bash_aliases.backup

mv ~/.bashrc ~/.bashrc.backup

touch  ~/.bashrc; touch  ~/.bash_aliases

stow -t ~ bash

<!-- stow -t ~ bash_aliases -->

( to test )

ls -l ~/.bashrc
ls -l ~/.bash_aliases



###########################

chmod +x /path/to/install-font.sh

https://www.nerdfonts.com/font-downloads

/install-font.sh https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/UbuntuMono.zip
