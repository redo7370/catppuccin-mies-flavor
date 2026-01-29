<h3 align="center">
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/><br/>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
	Catppuccin for <a href="https://www.kde.org/">KDE</a>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
</h3>

<p align="center">
    <a href="https://github.com/redo7370/catppuccin-mies-flavor/stargazers"><img src="https://img.shields.io/github/stars/redo7370/catppuccin-mies-flavor?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>
    <a href="https://github.com/redo7370/catppuccin-mies-flavor/issues"><img src="https://img.shields.io/github/issues/redo7370/catppuccin-mies-flavor?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>
    <a href="https://github.com/redo7370/catppuccin-mies-flavor/contributors"><img src="https://img.shields.io/github/contributors/redo7370/catppuccin-mies-flavor?colorA=363a4f&colorB=a6da95&style=for-the-badge"></a>
</p>

# Important
The Current Commit on main Contains an unfinished state of development which wasn't foreseen. I checked my history and no merges whcih could have caused this were made. I probably have made a mistake while resolving merge conflicts. Do not use the commits which still contain this important section for theme installation!

## Python Virtual Environment (for test-theme.py)

Um das Python-Preview-Tool zu nutzen:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**requirements.txt**
```
PyQt6
```

## Installation

### For KDE Plasma Desktop:
1. `git clone --depth=1 https://github.com/catppuccin/kde catppuccin-kde && cd catppuccin-kde`
2. Run the install script using `./install.sh` and follow the instructions.

### For Krita:
1. Download the colour-scheme zip file for your preferred flavour from the [release](https://github.com/catppuccin/kde/releases/) tab.
2. Extract the file and move the theme(s) you wish to install into the following folders for your platform:
   Windows: `%appdata%\krita\color-schemes`  
   Linux: `~/.local/share/krita/color-schemes`
3. Open Krita, and you can choose the theme from Settings > Themes.


## Notes
1. If you are using KDE 5.27 or below, you might want to run `git checkout v0.2.5`  before running the install script to avoid running into compatibility issues. Alternatively, the release binaries are available [here](https://github.com/catppuccin/kde/releases/tag/v0.2.5). (Does not support the mies flavor)
2. If you encounter an error similar to 'connection refused' while running the installation script, it may be due to store.kde.org being down or issues with your internet connection.



## 💝 Current Upstream Maintainer
- [Sourcastic](https://github.com/Sourcastic)

## 💝 Current Fork Maintainer
- [redo7370](https://github.com/redo7370)

## 💖 Past Maintainers
- [Prayag2](https://github.com/Prayag2)


&nbsp;

<p align="center"><img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/footers/gray0_ctp_on_line.svg?sanitize=true" /></p>
<p align="center">Copyright &copy; 2021-present <a href="https://github.com/catppuccin" target="_blank">Catppuccin Org</a>
<p align="center"><a href="https://github.com/catppuccin/catppuccin/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a></p>
