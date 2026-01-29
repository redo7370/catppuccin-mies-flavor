<h3 align="center">
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/><br/>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
	Catppuccin Mies Flavor for <a href="https://www.kde.org/">KDE</a>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
</h3>

<p align="center">
    <a href="https://github.com/redo7370/catppuccin-mies-flavor/stargazers"><img src="https://img.shields.io/github/stars/redo7370/catppuccin-mies-flavor?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>
    <a href="https://github.com/redo7370/catppuccin-mies-flavor/issues"><img src="https://img.shields.io/github/issues/redo7370/catppuccin-mies-flavor?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>
    <a href="https://github.com/redo7370/catppuccin-mies-flavor/contributors"><img src="https://img.shields.io/github/contributors/redo7370/catppuccin-mies-flavor?colorA=363a4f&colorB=a6da95&style=for-the-badge"></a>
</p>s

## Python Virtual Environment (for test-theme.py)

The python preview is not a 1:1 reconstruction of the KDE Theme but rather a Mock which can be utilized as orientation for the actual implementation.

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
1. `git clone https://github.com/catppuccin/kde catppuccin-kde && cd catppuccin-kde`
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
3. This theme is developed solely by myself. I will listen to community advice, but my primary long term target is to create a KDE Theme I like by targetting what I see as Catppuccins weaknesses and integrating other Themes strengths.
4. Since I'm developing mainly for my own benefit and to my own liking, there is no Update Schedule. Updates will come randomly and will most likely require you to newly clone/pull this repo from Github and install the theme again - Please note that for reinstallation you might have to remove the old theme files first, since there're sometimes issues with overwriting old files by simply running the install script.
5. Bugs or Feature Requests will only be accepted via Github Issues.
6. Shoutout to all devs of the original Catppuccin Themes and to [Juxtopposed](https://github.com/juxtopposed) whom I first saw using rectangular buttons for a more sleek design.

## Opacity Control
If you wish to have **transparent windows**, you must configure this yourself, as **KWin** controls window opacity. You can apply the basic **KWin ruleset** provided in this repository by going to **System Settings → Window Management → Window Rules** and clicking on **Import**, then importing the provided files. Please note that this is only a basic settings set and not an "out of the box" set of rules.

This ruleset by default makes all windows slightly transparent. If you open an app or game that has this opacity applied, you'll have to **exclude** it manually. This is possible by opening the window, pressing <kbd>Alt</kbd>+<kbd>F3</kbd>. A small drop-down menu should open. Click on **More Actions → Configure Special Application Settings**. A separate window will open which targets only the window you had active when pressing <kbd>Alt</kbd>+<kbd>F3</kbd>. Here you can click on **Add Property** and choose **Active Opacity** and **Inactive Opacity** to adjust them to your liking. Set both to **100%** if you want them to be solid.

It is recommended to do this one by one every time you open a window and realize you want it to be not transparent. If you don't want to do any of this at all, it is recommended you leave the **KWin rules** untouched at the cost of aesthetics.


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
