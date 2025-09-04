set -g fish_greeting

# source ~/.config/fish/hyde_config.fish

if type -q starship
    starship init fish | source
    set -gx STARSHIP_CACHE $XDG_CACHE_HOME/starship
    set -gx STARSHIP_CONFIG $XDG_CONFIG_HOME/starship/starship.toml
end

# fzf 
if type -q fzf
    fzf --fish | source
end

# example integration with bat : <cltr+f>
# bind -M insert \ce '$EDITOR $(fzf --preview="bat --color=always --plain {}")' 

set fish_pager_color_prefix cyan
set fish_color_autosuggestion brblack

# List Directory
alias l='eza -lh  --icons=auto' # long list
alias ls='eza -1   --icons=auto' # short list
alias ll='eza -lha --icons=auto --sort=name --group-directories-first' # long list all
alias ld='eza -lhD --icons=auto' # long list dirs
alias lt='eza --icons=auto --tree' # list folder as tree
alias vc='code'

alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gpush='git push'
alias gpull='git pull'

alias sleep='systemctl suspend'
alias hibernate='systemctl hibernate'

alias sunlab='sshfs les328@sunlab.cse.lehigh.edu:/home/les328/ ~/Documents/college/sunlab/'
alias sunlab_unmount='cd; fusermount3 -u ~/Documents/college/sunlab/'

# Handy change dir shortcuts
abbr .. 'cd ..'
abbr ... 'cd ../..'
abbr .3 'cd ../../..'
abbr .4 'cd ../../../..'
abbr .5 'cd ../../../../..'

# Always mkdir a path (this doesn't inhibit functionality to make a single dir)
abbr mkdir 'mkdir -p'
