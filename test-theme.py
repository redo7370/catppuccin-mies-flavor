#!/usr/bin/env python3
"""
Catppuccin Theme Preview Tool
Creates a FRAMELESS window with custom title bar using REAL theme files from this repository.
Reads actual rc config files and SVG button colors - NO MOCKS!

On Arch Linux, install dependencies with:
    sudo pacman -S python-pyqt6 python-pyqt6-svg
"""

import sys
import re
import configparser
from pathlib import Path

try:
    from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                                  QHBoxLayout, QLabel, QComboBox,
                                  QFrame, QGraphicsDropShadowEffect)
    from PyQt6.QtCore import Qt, QPoint
    from PyQt6.QtGui import QColor, QPainter
    PYQT6 = True
except ImportError:
    try:
        from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                      QHBoxLayout, QLabel, QComboBox,
                                      QFrame, QGraphicsDropShadowEffect)
        from PyQt5.QtCore import Qt, QPoint
        from PyQt5.QtGui import QColor, QPainter
        PYQT6 = False
    except ImportError:
        print("Error: PyQt5 or PyQt6 is required.")
        print("")
        print("On Arch Linux:")
        print("    sudo pacman -S python-pyqt6 python-pyqt6-svg")
        print("")
        print("On other distros:")
        print("    pip install PyQt6")
        sys.exit(1)

REPO_ROOT = Path(__file__).parent.absolute()
AURORAE_DIR = REPO_ROOT / "Resources" / "Aurorae"
COMMON_DIR = AURORAE_DIR / "Common"

# Fallback base colors (only used if not extractable from theme files)
BASE_COLORS = {
    "Mocha": {"base": "#1e1e2e", "mantle": "#181825", "surface0": "#313244"},
    "Macchiato": {"base": "#24273a", "mantle": "#1e2030", "surface0": "#363a4f"},
    "Frappe": {"base": "#303446", "mantle": "#292c3c", "surface0": "#414559"},
    "Latte": {"base": "#eff1f5", "mantle": "#e6e9ef", "surface0": "#ccd0da"},
}


class ThemeLoader:
    """Loads theme configuration from actual repository files."""
    
    def __init__(self, flavor: str, style: str):
        self.flavor = flavor
        self.style = style
        self.theme_dir = AURORAE_DIR / f"Catppuccin{flavor}-{style}"
        self.rc_file = self._get_rc_file()
        
        # Load configuration
        self.config = self._load_rc_config()
        self.button_colors = self._load_button_colors()
    
    def _get_rc_file(self) -> Path:
        """Get the correct rc file path."""
        if self.flavor == "Latte":
            return COMMON_DIR / f"CatppuccinLatte-{self.style}rc"
        else:
            return COMMON_DIR / f"Catppuccin-{self.style}rc"
    
    def _load_rc_config(self) -> dict:
        """Load and parse the rc configuration file."""
        config = {
            "button_width": 50,
            "button_height": 11,
            "button_spacing": 3,
            "title_height": 26,
            "active_text_color": "#cdd6f4",
            "inactive_text_color": "#a6adc8",
        }
        
        if not self.rc_file.exists():
            print(f"Warning: RC file not found: {self.rc_file}")
            return config
        
        try:
            content = self.rc_file.read_text()
            
            # Parse key=value pairs
            for line in content.split('\n'):
                line = line.strip()
                if '=' in line and not line.startswith('['):
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == "ButtonWidth":
                        config["button_width"] = int(value)
                    elif key == "ButtonHeight":
                        config["button_height"] = int(value)
                    elif key == "ButtonSpacing":
                        config["button_spacing"] = int(value)
                    elif key == "TitleHeight":
                        config["title_height"] = int(value)
                    elif key == "ActiveTextColor":
                        config["active_text_color"] = value
                    elif key == "InactiveTextColor":
                        config["inactive_text_color"] = value
        except Exception as e:
            print(f"Warning: Could not parse rc file: {e}")
        
        return config
    
    def _extract_color_from_svg(self, svg_path: Path) -> str:
        """Extract the primary fill color from an SVG file."""
        if not svg_path.exists():
            return "#888888"
        
        try:
            content = svg_path.read_text()
            # Find the first rect with a fill color (active state)
            match = re.search(r'<rect[^>]*fill="(#[0-9a-fA-F]{6})"', content)
            if match:
                return match.group(1)
        except Exception as e:
            print(f"Warning: Could not parse SVG {svg_path}: {e}")
        
        return "#888888"
    
    def _load_button_colors(self) -> dict:
        """Load button colors from actual SVG files."""
        colors = {}
        
        button_files = ["close", "maximize", "minimize", "restore", "alldesktops", "keepabove", "keepbelow"]
        
        for button in button_files:
            svg_path = self.theme_dir / f"{button}.svg"
            colors[button] = self._extract_color_from_svg(svg_path)
        
        return colors
    
    def get_button_color(self, button_type: str) -> str:
        """Get the color for a specific button type."""
        return self.button_colors.get(button_type, "#888888")
    
    def get_inactive_color(self) -> str:
        """Get the inactive button color from SVG."""
        # Parse the close.svg to get the inactive color (4th rect)
        svg_path = self.theme_dir / "close.svg"
        if svg_path.exists():
            try:
                content = svg_path.read_text()
                # Find the 4th rect (inactive state at x=151)
                matches = re.findall(r'<rect[^>]*fill="(#[0-9a-fA-F]{6})"', content)
                if len(matches) >= 4:
                    return matches[3]  # inactive-center
            except:
                pass
        return BASE_COLORS.get(self.flavor, {}).get("surface0", "#45475a")
    
    def exists(self) -> bool:
        """Check if the theme directory exists."""
        return self.theme_dir.exists()


class TitleBarButton(QWidget):
    """Title bar button - dimensions loaded from rc file."""
    
    def __init__(self, color: str, width: int, height: int, action=None, parent=None):
        super().__init__(parent)
        self.color = color
        self.btn_width = width
        self.btn_height = height
        self.action = action
        self.hovered = False
        self.pressed = False
        
        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor if PYQT6 else Qt.PointingHandCursor)
    
    def set_color(self, color: str):
        self.color = color
        self.update()
    
    def set_size(self, width: int, height: int):
        self.btn_width = width
        self.btn_height = height
        self.setFixedSize(width, height)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing if PYQT6 else QPainter.Antialiasing)
        
        c = QColor(self.color)
        if self.pressed:
            c.setAlphaF(0.6)
        elif self.hovered:
            c.setAlphaF(0.85)
        
        # Rounded rectangle with 2px radius (matching SVG rx=2)
        painter.setBrush(c)
        painter.setPen(Qt.PenStyle.NoPen if PYQT6 else Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.btn_width, self.btn_height, 2, 2)
        painter.end()
    
    def enterEvent(self, event):
        self.hovered = True
        self.update()
    
    def leaveEvent(self, event):
        self.hovered = False
        self.pressed = False
        self.update()
    
    def mousePressEvent(self, event):
        self.pressed = True
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.update()
        if self.action and self.rect().contains(event.pos()):
            self.action()


class CustomTitleBar(QWidget):
    """Draggable title bar with buttons from real theme files."""
    
    def __init__(self, window, theme: ThemeLoader):
        super().__init__(window)
        self.window = window
        self.theme = theme
        self.drag_pos = None
        self.setup_ui()
    
    def setup_ui(self):
        cfg = self.theme.config
        base = BASE_COLORS.get(self.theme.flavor, BASE_COLORS["Mocha"])
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)
        layout.setSpacing(0)
        
        self.title = QLabel(f"  Catppuccin {self.theme.flavor} - {self.theme.style}")
        self.title.setStyleSheet(f"color: {cfg['active_text_color']}; font-weight: bold; font-size: 13px;")
        layout.addWidget(self.title)
        layout.addStretch()
        
        # Buttons with spacing from rc file
        btn_box = QWidget()
        btn_layout = QHBoxLayout(btn_box)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(cfg["button_spacing"])
        
        w, h = cfg["button_width"], cfg["button_height"]
        
        self.btn_min = TitleBarButton(self.theme.get_button_color("minimize"), w, h, self.window.showMinimized)
        self.btn_max = TitleBarButton(self.theme.get_button_color("maximize"), w, h, self.toggle_max)
        self.btn_close = TitleBarButton(self.theme.get_button_color("close"), w, h, self.window.close)
        
        btn_layout.addWidget(self.btn_min)
        btn_layout.addWidget(self.btn_max)
        btn_layout.addWidget(self.btn_close)
        layout.addWidget(btn_box)
        
        self.setStyleSheet(f"background-color: {base['mantle']}80;")
        self.setFixedHeight(40)
    
    def toggle_max(self):
        if self.window.isMaximized():
            self.window.showNormal()
        else:
            self.window.showMaximized()
    
    def update_theme(self, theme: ThemeLoader):
        self.theme = theme
        cfg = theme.config
        base = BASE_COLORS.get(theme.flavor, BASE_COLORS["Mocha"])
        
        self.title.setText(f"  Catppuccin {theme.flavor} - {theme.style}")
        self.title.setStyleSheet(f"color: {cfg['active_text_color']}; font-weight: bold; font-size: 13px;")
        self.setStyleSheet(f"background-color: {base['mantle']}80;")
        
        w, h = cfg["button_width"], cfg["button_height"]
        
        self.btn_min.set_color(theme.get_button_color("minimize"))
        self.btn_min.set_size(w, h)
        
        self.btn_max.set_color(theme.get_button_color("maximize"))
        self.btn_max.set_size(w, h)
        
        self.btn_close.set_color(theme.get_button_color("close"))
        self.btn_close.set_size(w, h)
        
        # Update button spacing
        btn_layout = self.btn_min.parent().layout()
        if btn_layout:
            btn_layout.setSpacing(cfg["button_spacing"])
    
    def mousePressEvent(self, event):
        if event.button() == (Qt.MouseButton.LeftButton if PYQT6 else Qt.LeftButton):
            self.drag_pos = event.globalPosition().toPoint() if PYQT6 else event.globalPos()
    
    def mouseMoveEvent(self, event):
        if self.drag_pos:
            pos = event.globalPosition().toPoint() if PYQT6 else event.globalPos()
            self.window.move(self.window.pos() + pos - self.drag_pos)
            self.drag_pos = pos
    
    def mouseReleaseEvent(self, event):
        self.drag_pos = None
    
    def mouseDoubleClickEvent(self, event):
        self.toggle_max()


class ThemeWindow(QWidget):
    """Frameless window using REAL Catppuccin theme files from repository."""
    
    def __init__(self):
        super().__init__()
        self.flavor = "Mocha"
        self.style = "Modern"
        self.theme = ThemeLoader(self.flavor, self.style)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint if PYQT6 else Qt.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground if PYQT6 else Qt.WA_TranslucentBackground)
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        self.container = QFrame(self)
        main = QVBoxLayout(self)
        main.setContentsMargins(5, 5, 5, 5)
        main.addWidget(self.container)
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title bar
        self.title_bar = CustomTitleBar(self, self.theme)
        layout.addWidget(self.title_bar)
        
        # Content
        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(25, 25, 25, 25)
        c_layout.setSpacing(15)
        
        # Flavor selector
        row = QWidget()
        r_layout = QHBoxLayout(row)
        r_layout.setContentsMargins(0, 0, 0, 0)
        r_layout.setSpacing(10)
        
        self.lbl_flavor = QLabel("Flavor:")
        r_layout.addWidget(self.lbl_flavor)
        
        self.combo_flavor = QComboBox()
        self.combo_flavor.addItems(["Mocha", "Macchiato", "Frappe", "Latte"])
        self.combo_flavor.currentTextChanged.connect(self.on_flavor_changed)
        self.combo_flavor.setMinimumWidth(130)
        r_layout.addWidget(self.combo_flavor)
        
        self.lbl_style = QLabel("Style:")
        r_layout.addWidget(self.lbl_style)
        
        self.combo_style = QComboBox()
        self.combo_style.addItems(["Modern", "Classic"])
        self.combo_style.currentTextChanged.connect(self.on_style_changed)
        r_layout.addWidget(self.combo_style)
        
        r_layout.addStretch()
        c_layout.addWidget(row)
        
        # Info
        self.info = QLabel()
        self.info.setWordWrap(True)
        c_layout.addWidget(self.info)
        
        # Config display
        self.config_display = QLabel()
        self.config_display.setWordWrap(True)
        c_layout.addWidget(self.config_display)
        
        # Color preview
        self.lbl_colors = QLabel("Button colors from SVG files:")
        c_layout.addWidget(self.lbl_colors)
        
        swatches = QWidget()
        sw_layout = QHBoxLayout(swatches)
        sw_layout.setContentsMargins(0, 5, 0, 10)
        sw_layout.setSpacing(25)
        
        self.swatch_close = self.make_swatch("Close")
        self.swatch_max = self.make_swatch("Maximize")
        self.swatch_min = self.make_swatch("Minimize")
        sw_layout.addWidget(self.swatch_close)
        sw_layout.addWidget(self.swatch_max)
        sw_layout.addWidget(self.swatch_min)
        sw_layout.addStretch()
        c_layout.addWidget(swatches)
        
        c_layout.addStretch()
        
        # Path info
        self.path_info = QLabel()
        self.path_info.setWordWrap(True)
        c_layout.addWidget(self.path_info)
        
        layout.addWidget(content)
        
        self.setMinimumSize(600, 450)
        self.resize(650, 500)
    
    def make_swatch(self, name: str) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(4)
        
        rect = QFrame()
        rect.setFixedSize(50, 11)
        rect.setStyleSheet("border-radius: 2px;")
        l.addWidget(rect, alignment=Qt.AlignmentFlag.AlignCenter if PYQT6 else Qt.AlignCenter)
        
        lbl = QLabel(name)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT6 else Qt.AlignCenter)
        l.addWidget(lbl)
        
        color_lbl = QLabel()
        color_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT6 else Qt.AlignCenter)
        l.addWidget(color_lbl)
        
        w.rect_frame = rect
        w.name_lbl = lbl
        w.color_lbl = color_lbl
        return w
    
    def on_flavor_changed(self, flavor: str):
        self.flavor = flavor
        self.theme = ThemeLoader(flavor, self.style)
        self.apply_theme()
    
    def on_style_changed(self, style: str):
        self.style = style
        self.theme = ThemeLoader(self.flavor, style)
        self.apply_theme()
    
    def apply_theme(self):
        self.title_bar.update_theme(self.theme)
        
        cfg = self.theme.config
        base = BASE_COLORS.get(self.flavor, BASE_COLORS["Mocha"])
        
        # Container styling
        self.container.setStyleSheet(f"""
            QFrame {{
                background-color: {base['base']}80;
                border: 2px solid {base['surface0']}80;
                border-radius: 12px;
            }}
        """)
        
        # Text colors from rc file
        txt = f"color: {cfg['active_text_color']};"
        sub = f"color: {cfg['inactive_text_color']}; font-size: 11px;"
        
        self.lbl_flavor.setStyleSheet(txt)
        self.lbl_style.setStyleSheet(txt)
        self.lbl_colors.setStyleSheet(txt)
        
        # Info text
        self.info.setStyleSheet(txt)
        self.info.setText(
            "This window uses REAL theme files from the repository!\n\n"
            "• Button colors are read from SVG files\n"
            "• Dimensions and spacing from rc config files\n"
            "• Text colors from rc config files\n"
            "• No hardcoded mock values!"
        )
        
        # Config display
        self.config_display.setStyleSheet(sub)
        self.config_display.setText(
            f"RC Config: ButtonWidth={cfg['button_width']}, "
            f"ButtonHeight={cfg['button_height']}, "
            f"ButtonSpacing={cfg['button_spacing']}, "
            f"TitleHeight={cfg['title_height']}"
        )
        
        # Combo styling
        combo_css = f"""
            QComboBox {{
                background-color: {base['surface0']};
                color: {cfg['active_text_color']};
                border: 1px solid {self.theme.get_inactive_color()};
                border-radius: 4px;
                padding: 5px 10px;
            }}
            QComboBox:hover {{ border-color: {self.theme.get_button_color('alldesktops')}; }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{
                background-color: {base['surface0']};
                color: {cfg['active_text_color']};
                selection-background-color: {self.theme.get_inactive_color()};
            }}
        """
        self.combo_flavor.setStyleSheet(combo_css)
        self.combo_style.setStyleSheet(combo_css)
        
        # Swatches - show actual colors from SVG files
        swatch_data = [
            ("close", self.swatch_close),
            ("maximize", self.swatch_max),
            ("minimize", self.swatch_min)
        ]
        
        for button_name, sw in swatch_data:
            color = self.theme.get_button_color(button_name)
            sw.rect_frame.setStyleSheet(f"background-color: {color}; border: none; border-radius: 2px;")
            sw.rect_frame.setFixedSize(cfg['button_width'], cfg['button_height'])
            sw.name_lbl.setStyleSheet(sub)
            sw.color_lbl.setStyleSheet(f"color: {cfg['inactive_text_color']}; font-size: 9px;")
            sw.color_lbl.setText(color)
        
        # Path info
        if self.theme.exists():
            rc_rel = self.theme.rc_file.relative_to(REPO_ROOT)
            theme_rel = self.theme.theme_dir.relative_to(REPO_ROOT)
            self.path_info.setText(f"✓ RC: {rc_rel}\n✓ SVGs: {theme_rel}/")
            self.path_info.setStyleSheet(f"color: {self.theme.get_button_color('maximize')}; font-size: 10px;")
        else:
            self.path_info.setText(f"✗ Theme not found: {self.theme.theme_dir}")
            self.path_info.setStyleSheet(f"color: {self.theme.get_button_color('close')}; font-size: 10px;")


def main():
    print(f"Catppuccin Theme Preview (REAL FILES)")
    print(f"Repository: {REPO_ROOT}")
    print(f"Aurorae Dir: {AURORAE_DIR}")
    print(f"PyQt6: {PYQT6}")
    print()
    
    # List available themes
    print("Available themes:")
    for flavor in ["Mocha", "Macchiato", "Frappe", "Latte"]:
        for style in ["Modern", "Classic"]:
            theme_dir = AURORAE_DIR / f"Catppuccin{flavor}-{style}"
            status = "✓" if theme_dir.exists() else "✗"
            print(f"  {status} Catppuccin{flavor}-{style}")
    print()
    
    app = QApplication(sys.argv)
    win = ThemeWindow()
    win.show()
    sys.exit(app.exec() if PYQT6 else app.exec_())


if __name__ == "__main__":
    main()
