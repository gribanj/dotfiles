sudo apt-get update -y
sudo apt-get install cmake -y
sudo apt-get install fzf -y
sudo apt-get install stow -y
cargo install eza

brew install jesseduffield/lazydocker/lazydocker
brew install eza

cargo install zoxide
zoxide init nu > ~/.zoxide.nu

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

# https://thevaluable.dev/fzf-shell-integration/

in nushell run:
sudo apt-get install fzf -y
mkdir ~/.config/fzf
fzf init nu | save ~/.config/fzf/init.nu
