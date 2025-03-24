#################################
# CUSTOM SETTING YG #
#################################

highlightExitCode() {
    exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo -en '\xf0\x9f\x98\xb1 '  # Sad face for non-zero exit codes
    else
        echo -en '\xf0\x9f\x98\x80 '  # Smiley face for zero exit code
    fi
}

PS1='${VIRTUAL_ENV_PROMPT:+$VIRTUAL_ENV_PROMPT}\[\e[1;32m\]$(highlightExitCode) [\A]\[\e[m\] \$ '

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

#################################

eval "$(direnv hook bash)"
# Modify the shell prompt to include the virtual environment if active
# PS1='${VIRTUAL_ENV_PROMPT:+($VIRTUAL_ENV_PROMPT)}[\w]\n\$ '

#################################
source /usr/share/bash-completion/bash_completion
source /etc/bash_completion
# source <(make completion bash)
alias m=make
complete -F __start_make m

#################################

source /usr/share/bash-completion/bash_completion
source /etc/bash_completion
# source <(terraform completion bash)
alias t=terraform
complete -F __start_terraform t

#################################

source /usr/share/bash-completion/bash_completion
source /etc/bash_completion
source <(docker completion bash)
alias d=docker
complete -F __start_docker d

#################################

#alias terraform='docker run --rm -it -w /workspace -v ~/.aws/credentials:/root/.aws/credentials:ro -e AWS_PROFILE=yg_personal  -v $PWD:/workspace hashicorp/terraform:latest'

alias t='docker run --rm -it -w /workspace -v ~/.aws/credentials:/root/.aws/credentials:ro -e AZURE_SUBSCRIPTION_ID=bde1b843-30b0-42f5-8c57-d70991cdf132  -e AWS_PROFILE=yg_personal  -v $PWD:/workspace hashicorp/terraform:latest'

# alias az='docker run --rm -it -v $HOME/.azure:/root/.azure -v $PWD:/workspace -w /workspace mcr.microsoft.com/azure-cli az'

alias c='docker run --rm -it -v $PWD:/workspace -w /workspace bridgecrew/checkov'

alias tflint='docker run --rm -it -v $PWD:/workspace -w /workspace ghcr.io/terraform-linters/tflint'

alias vault='docker run --rm -it -v $PWD:/vault -w /vault hashicorp/docker-vault:latest'

alias v='docker run --rm -it -v $PWD:/vault -w /vault vault:latest'

alias dive="docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive"
# e.g. dive <your-image-tag>


eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"



# alias terraform='docker run --rm -it -w /workspace -v ~/.aws/credentials:/root/.aws/credentials:ro -e AWS_PROFILE=yg_personal  -v $PWD:/workspace hashicorp/terraform:latest'

# alias t='docker run --rm -it -w /workspace -v ~/.aws/credentials:/root/.aws/credentials:ro -e AZURE_SUBSCRIPTION_ID=bde1b843-30b0-42f5-8c57-d70991cdf132  -e AWS_PROFILE=yg_personal  -v $PWD:/workspace hashicorp/terraform:latest'

# alias az='docker run --rm -it -v $HOME/.azure:/root/.azure -v $PWD:/workspace -w /workspace mcr.microsoft.com/azure-cli az'

# alias c='docker run --rm -it -v $PWD:/workspace -w /workspace bridgecrew/checkov'

# alias tflint='docker run --rm -it -v $PWD:/workspace -w /workspace ghcr.io/terraform-linters/tflint'

# alias vault='docker run --rm -it -v $PWD:/vault -w /vault hashicorp/docker-vault:latest'

# alias v='docker run --rm -it -v $PWD:/vault -w /vault vault:latest'

# . "$HOME/.cargo/env"
