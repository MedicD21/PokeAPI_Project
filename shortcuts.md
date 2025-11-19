#############################################
#   OH-MY-POSH THEME (macOS optimized)      #
#############################################

# Load only in interactive shells to prevent widget errors
if [[ $- == *i* ]]; then
    eval "$(oh-my-posh init zsh --config /usr/local/opt/oh-my-posh/themes/dev-minimal.omp.json)"
fi

#############################################
#             BASIC ALIASES                 #
#############################################

alias ll="ls -al"
alias la="ls -a"
alias clr="clear"

up()  { cd ..; pwd }
up2() { cd ../..; pwd }

#############################################
#             GIT SHORTCUTS                 #
#############################################

alias gstatus="git status"
alias gadd="git add"
alias gcommit="git commit"
alias gpush="git push"
alias gpull="git pull"
alias gbranch="git branch"
alias gcheckout="git checkout"
alias glg="git log --oneline --graph --decorate --all"

#############################################
#             GIT POWER TOOLS               #
#############################################

gfix() {
    git add -A
    git commit -m "$1"
    git push
    echo "✓ Auto stage + commit + push complete!"
}

gundo() {
    git reset HEAD~1
    echo "✓ Reverted last commit (kept changes)"
}

gsync() {
    git pull --rebase
    git push
    echo "✓ Synced with remote"
}

#############################################
#      AUTO PYTHON VENV ACTIVATION          #
#############################################

auto_activate_venv() {
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        echo "(venv activated)"
    fi
}

# Fires every time directory changes
chpwd() { auto_activate_venv }
auto_activate_venv

#############################################
#              MKVENV TOOL                  #
#############################################

mkvenv() {
    echo "🔧 Creating Python venv..."
    python3 -m venv .venv

    if [ ! -f ".venv/bin/activate" ]; then
        echo "❌ Failed to create .venv"
        return
    fi

    echo "⚡ Activating..."
    source .venv/bin/activate

    echo "📦 Installing dev tools..."
    pip install --upgrade pip
    pip install black ruff uv ipykernel

    echo "🎉 Virtual environment ready!"
}

#############################################
#             PATH CLEANUP                  #
#############################################

export PATH="$HOME/.local/bin:$PATH"
