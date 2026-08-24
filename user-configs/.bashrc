#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '
export PATH="/mnt/dados/node/bin:$PATH"
export PATH="$PATH:$HOME/.local/bin"

# OmniRoute API Key para OpenCode
export OMNIROUTE_API_KEY="sk-68bd79a65373a1aa-68a842-e13bfca2"

# Ollama Configuration
export OLLAMA_KV_CACHE_TYPE=q8_0
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_KEEP_ALIVE=30s
