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

#PS1='${VIRTUAL_ENV_PROMPT:+$VIRTUAL_ENV_PROMPT}\[\e[1;32m\]$(highlightExitCode) [\A]\[\e[m\] \$ '

#PS1='${VIRTUAL_ENV_PROMPT:+$VIRTUAL_ENV_PROMPT}\[\e[1;32m\]$(highlightExitCode) \[\e[m\] \$ '

#PS1='${VIRTUAL_ENV_PROMPT:+$VIRTUAL_ENV_PROMPT}\[\e[1;32m\]$(highlightExitCode) \[\e[m\] '

PS1='${VIRTUAL_ENV_PROMPT:+$VIRTUAL_ENV_PROMPT}\[\e[1;32m\]$(highlightExitCode)⏵ \[\e[m\]'

#PS1='${VIRTUAL_ENV_PROMPT:+$VIRTUAL_ENV_PROMPT}\[\e[1;32m\]$(highlightExitCode) \[\e[m\]⏵'

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


################################# GIT ALIASES #################################

alias gc="git commit -m"
alias gca="git commit -a -m"
alias gp="git push origin HEAD"
alias gpu="git pull origin"
alias gst="git status"
alias glog="git log --graph --topo-order --pretty='%w(100,0,6)%C(yellow)%h%C(bold)%C(black)%d %C(cyan)%ar %C(green)%an%n%C(bold)%C(white)%s %N' --abbrev-commit"
alias gdiff="git diff"
alias gco="git checkout"
alias gb="git branch"
alias gba="git branch -a"
alias gadd="git add"
alias ga="git add -p"
alias gcoall="git checkout -- ."
alias gr="git remote"
alias gre="git reset"

################################# ALIAS FOR COMMON COMMANDS #################################

alias l='ls --all'
alias c='clear'
alias cls='clear'
alias ll='ls -l'
alias lt='eza --tree --level=2 --long --icons --git'
alias v='nvim'
alias u='sudo apt update && sudo apt upgrade -y'
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

# alias t='docker run --rm -it -w /workspace -v ~/.aws/credentials:/root/.aws/credentials:ro -e AZURE_SUBSCRIPTION_ID=bde1b843-30b0-42f5-8c57-d70991cdf132  -e AWS_PROFILE=yg_personal  -v $PWD:/workspace hashicorp/terraform:latest'

alias t='docker run --rm -it -v $PWD:/workspace -w /workspace hashicorp/terraform:latest'

# alias az='docker run --rm -it -v $HOME/.azure:/root/.azure -v $PWD:/workspace -w /workspace mcr.microsoft.com/azure-cli az'

alias check='docker run --rm -it -v $PWD:/workspace -w /workspace bridgecrew/checkov'

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

# shellcheck shell=bash

################################# ZOXIDE ######################################
# =============================================================================
#
# Utility functions for zoxide.
#

# pwd based on the value of _ZO_RESOLVE_SYMLINKS.
function __zoxide_pwd() {
    \builtin pwd -L
}

# cd + custom logic based on the value of _ZO_ECHO.
function __zoxide_cd() {
    # shellcheck disable=SC2164
    \builtin cd -- "$@"
}

# =============================================================================
#
# Hook configuration for zoxide.
#

# Hook to add new entries to the database.
__zoxide_oldpwd="$(__zoxide_pwd)"

function __zoxide_hook() {
    \builtin local -r retval="$?"
    \builtin local pwd_tmp
    pwd_tmp="$(__zoxide_pwd)"
    if [[ ${__zoxide_oldpwd} != "${pwd_tmp}" ]]; then
        __zoxide_oldpwd="${pwd_tmp}"
        \command zoxide add -- "${__zoxide_oldpwd}"
    fi
    return "${retval}"
}

# Initialize hook.
if [[ ${PROMPT_COMMAND:=} != *'__zoxide_hook'* ]]; then
    PROMPT_COMMAND="__zoxide_hook;${PROMPT_COMMAND#;}"
fi

# Report common issues.
function __zoxide_doctor() {
    [[ ${_ZO_DOCTOR:-1} -ne 0 ]] || return 0
    [[ ${PROMPT_COMMAND:=} != *'__zoxide_hook'* ]] || return 0

    _ZO_DOCTOR=0
    \builtin printf '%s\n' \
        'zoxide: detected a possible configuration issue.' \
        'Please ensure that zoxide is initialized right at the end of your shell configuration file (usually ~/.bashrc).' \
        '' \
        'If the issue persists, consider filing an issue at:' \
        'https://github.com/ajeetdsouza/zoxide/issues' \
        '' \
        'Disable this message by setting _ZO_DOCTOR=0.' \
        '' >&2
}

# =============================================================================
#
# When using zoxide with --no-cmd, alias these internal functions as desired.
#

__zoxide_z_prefix='z#'

# Jump to a directory using only keywords.
function __zoxide_z() {
    __zoxide_doctor

    # shellcheck disable=SC2199
    if [[ $# -eq 0 ]]; then
        __zoxide_cd ~
    elif [[ $# -eq 1 && $1 == '-' ]]; then
        __zoxide_cd "${OLDPWD}"
    elif [[ $# -eq 1 && -d $1 ]]; then
        __zoxide_cd "$1"
    elif [[ $# -eq 2 && $1 == '--' ]]; then
        __zoxide_cd "$2"
    elif [[ ${@: -1} == "${__zoxide_z_prefix}"?* ]]; then
        # shellcheck disable=SC2124
        \builtin local result="${@: -1}"
        __zoxide_cd "${result:${#__zoxide_z_prefix}}"
    else
        \builtin local result
        # shellcheck disable=SC2312
        result="$(\command zoxide query --exclude "$(__zoxide_pwd)" -- "$@")" &&
            __zoxide_cd "${result}"
    fi
}

# Jump to a directory using interactive search.
function __zoxide_zi() {
    __zoxide_doctor
    \builtin local result
    result="$(\command zoxide query --interactive -- "$@")" && __zoxide_cd "${result}"
}

# =============================================================================
#
# Commands for zoxide. Disable these using --no-cmd.
#

\builtin unalias z &>/dev/null || \builtin true
function z() {
    __zoxide_z "$@"
}

\builtin unalias zi &>/dev/null || \builtin true
function zi() {
    __zoxide_zi "$@"
}

# Load completions.
# - Bash 4.4+ is required to use `@Q`.
# - Completions require line editing. Since Bash supports only two modes of
#   line editing (`vim` and `emacs`), we check if either them is enabled.
# - Completions don't work on `dumb` terminals.
if [[ ${BASH_VERSINFO[0]:-0} -eq 4 && ${BASH_VERSINFO[1]:-0} -ge 4 || ${BASH_VERSINFO[0]:-0} -ge 5 ]] &&
    [[ :"${SHELLOPTS}": =~ :(vi|emacs): && ${TERM} != 'dumb' ]]; then
    # Use `printf '\e[5n'` to redraw line after fzf closes.
    \builtin bind '"\e[0n": redraw-current-line' &>/dev/null

    function __zoxide_z_complete() {
        # Only show completions when the cursor is at the end of the line.
        [[ ${#COMP_WORDS[@]} -eq $((COMP_CWORD + 1)) ]] || return

        # If there is only one argument, use `cd` completions.
        if [[ ${#COMP_WORDS[@]} -eq 2 ]]; then
            \builtin mapfile -t COMPREPLY < <(
                \builtin compgen -A directory -- "${COMP_WORDS[-1]}" || \builtin true
            )
        # If there is a space after the last word, use interactive selection.
        elif [[ -z ${COMP_WORDS[-1]} ]] && [[ ${COMP_WORDS[-2]} != "${__zoxide_z_prefix}"?* ]]; then
            \builtin local result
            # shellcheck disable=SC2312
            result="$(\command zoxide query --exclude "$(__zoxide_pwd)" --interactive -- "${COMP_WORDS[@]:1:${#COMP_WORDS[@]}-2}")" &&
                COMPREPLY=("${__zoxide_z_prefix}${result}/")
            \builtin printf '\e[5n'
        fi
    }

    \builtin complete -F __zoxide_z_complete -o filenames -- z
    \builtin complete -r zi &>/dev/null || \builtin true
fi

# =============================================================================
#
# To initialize zoxide, add this to your shell configuration file (usually ~/.bashrc):
#
eval "$(zoxide init bash)"
