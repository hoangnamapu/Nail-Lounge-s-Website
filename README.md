1. Cloning github repo

```zsh
mkdir ~/Desktop/Panda/PoshApp
cd ~/Desktop/Panda/PoshApp
git clone
```

2. Install Homebrew & pyenv

```zsh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install pyenv
brew install pyenv-virtualenv
```

3. Setting up pyenv

```zsh
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
```

Then, restart terminal

4. Install & and set up new python environment

```zsh
pyenv install 3.12.1
pyenv virtualenv 3.12.1 Panda-PoshApp
echo 'alias PoshApp="cd ~/Desktop/Panda/PoshApp && pyenv activate Panda-PoshApp"' >> ~/.zshrc
source ~/.zshrc
```

5. Activate the python environment and start working

```zsh
PoshApp
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
