#!/usr/bin/env python3
"""
Catppuccin Theme Preview Tool
Creates a FRAMELESS window with custom title bar using theme from this repository.
The window itself displays the theme - the title bar buttons ARE the 10:1 rectangles!

On Arch Linux, install dependencies with:
    sudo pacman -S python-pyqt6 python-pyqt6-svg
"""

import sys
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

# Official Catppuccin colors
PALETTES = {
    "Mocha": {
        "base": "#1e1e2e", "mantle": "#181825", "crust": "#11111b",
        "surface0": "#313244", "surface1": "#45475a", "surface2": "#585b70",
        "overlay0": "#6c7086", "overlay1": "#7f849c",
        "text": "#cdd6f4", "subtext0": "#a6adc8",
        "red": "#f38ba8", "green": "#a6e3a1", "peach": "#fab387", "blue": "#89b4fa",
    },
    "Macchiato": {
        "base": "#24273a", "mantle": "#1e2030", "crust": "#181926",
        "surface0": "#363a4f", "surface1": "#494d64", "surface2": "#5b6078",
        "overlay0": "#6e738d", "overlay1": "#8087a2",
        "text": "#cad3f5", "subtext0": "#a5adcb",
        "red": "#ed8796", "green": "#a6da95", "peach": "#f5a97f", "blue": "#8aadf4",
    },
    "Frappe": {
        "base": "#303446", "mantle": "#292c3c", "crust": "#232634",
        "surface0": "#414559", "surface1": "#51576d", "surface2": "#626880",
        "overlay0": "#737994", "overlay1": "#838ba7",
        "text": "#c6d0f5", "subtext0": "#a5adce",
        "red": "#e78284", "green": "#a6d189", "peach": "#ef9f76", "blue": "#8caaee",
    },
    "Latte": {
        "base": "#eff1f5", "mantle": "#e6e9ef", "crust": "#dce0e8",
        "surface0": "#ccd0da", "surface1": "#bcc0cc", "surface2": "#acb0be",
        "overlay0": "#9ca0b0", "overlay1": "#8c8fa1",
        "text": "#4c4f69", "subtext0": "#6c6f85",
        "red": "#d20f39", "green": "#40a02b", "peach": "#fe640b", "blue": "#1e66f5",
    },
}


class TitleBarButton(QWidget):
    """Title bar button - rounded rectangle, no background"""
    
    def __init__(self, color: str, hover_bg: str, action=None, parent=None):
        super().__init__(parent)
        self.color = color
        self.hover_bg = hover_bg  # unused now
        self.action = action
        self.hovered = False
        self.pressed = False
        
        self.setFixedSize(50, 11)
        self.setCursor(Qt.CursorShape.PointingHandCursor if PYQT6 else Qt.PointingHandCursor)
    
    def set_color(self, color: str, hover_bg: str):
        self.color = color
        self.hover_bg = hover_bg
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing if PYQT6 else QPainter.Antialiasing)
        
        # Determine opacity based on state
        c = QColor(self.color)
        if self.pressed:
            c.setAlphaF(0.6)
        elif self.hovered:
            c.setAlphaF(0.85)
        
        # Rounded rectangle (50x11 with 2px radius)
        painter.setBrush(c)
        painter.setPen(Qt.PenStyle.NoPen if PYQT6 else Qt.NoPen)
        painter.drawRoundedRect(0, 0, 50, 11, 2, 2)
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
    """Draggable title bar with Catppuccin buttons"""
    
    def __init__(self, window, flavor: str):
        super().__init__(window)
        self.window = window
        self.flavor = flavor
        self.drag_pos = None
        self.setup_ui()
    
    def setup_ui(self):
        p = PALETTES[self.flavor]
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)
        layout.setSpacing(0)
        
        self.title = QLabel(f"  Catppuccin {self.flavor}")
        self.title.setStyleSheet(f"color: {p['text']}; font-weight: bold; font-size: 13px;")
        layout.addWidget(self.title)
        layout.addStretch()
        
        # Buttons with 3px spacing
        btn_box = QWidget()
        btn_layout = QHBoxLayout(btn_box)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(3)
        
        self.btn_min = TitleBarButton(p['peach'], p['surface0'] + "80", self.window.showMinimized)
        self.btn_max = TitleBarButton(p['green'], p['surface0'] + "80", self.toggle_max)
        self.btn_close = TitleBarButton(p['red'], p['surface0'] + "80", self.window.close)
        
        btn_layout.addWidget(self.btn_min)
        btn_layout.addWidget(self.btn_max)
        btn_layout.addWidget(self.btn_close)
        layout.addWidget(btn_box)
        
        self.setStyleSheet(f"background-color: {p['mantle']};")
        self.setFixedHeight(40)
    
    def toggle_max(self):
        if self.window.isMaximized():
            self.window.showNormal()
        else:
            self.window.showMaximized()
    
    def update_flavor(self, flavor: str):
        self.flavor = flavor
        p = PALETTES[flavor]
        self.title.setText(f"  Catppuccin {flavor}")
        self.title.setStyleSheet(f"color: {p['text']}; font-weight: bold; font-size: 13px;")
        self.setStyleSheet(f"background-color: {p['mantle']};")
        
        self.btn_min.set_color(p['peach'], p['surface0'] + "80")
        self.btn_max.set_color(p['green'], p['surface0'] + "80")
        self.btn_close.set_color(p['red'], p['surface0'] + "80")
    
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
    """Frameless window using Catppuccin theme from repository"""
    
    def __init__(self):
        super().__init__()
        self.flavor = "Mocha"
        self.style = "Modern"
        
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
        self.title_bar = CustomTitleBar(self, self.flavor)
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
        self.info = QLabel(
            "This window IS the theme preview!\n\n"
            "• The title bar uses Catppuccin colors from the repository\n"
            "• Buttons are rounded rectangles (50×11 px, 2px radius)\n"
            "• 3px spacing between buttons, no background on hover\n"
            "• Colors: Close=Red, Maximize=Green, Minimize=Peach\n"
            "• Drag the title bar to move the window"
        )
        self.info.setWordWrap(True)
        c_layout.addWidget(self.info)
        
        # Color preview
        self.lbl_colors = QLabel("Button colors in this flavor:")
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
        
        self.setMinimumSize(550, 380)
        self.resize(600, 420)
    
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
        
        w.rect_frame = rect
        w.name_lbl = lbl
        return w
    
    def on_flavor_changed(self, flavor: str):
        self.flavor = flavor
        self.apply_theme()
    
    def on_style_changed(self, style: str):
        self.style = style
        self.apply_theme()
    
    def apply_theme(self):
        p = PALETTES[self.flavor]
        self.title_bar.update_flavor(self.flavor)
        
        # Container with border
        self.container.setStyleSheet(f"""
            QFrame {{
                background-color: {p['base']};
                border: 2px solid {p['surface1']};
                border-radius: 12px;
            }}
        """)
        
        # Text colors
        txt = f"color: {p['text']};"
        sub = f"color: {p['subtext0']}; font-size: 11px;"
        
        self.lbl_flavor.setStyleSheet(txt)
        self.lbl_style.setStyleSheet(txt)
        self.lbl_colors.setStyleSheet(txt)
        self.info.setStyleSheet(txt)
        self.path_info.setStyleSheet(f"color: {p['overlay1']}; font-size: 10px;")
        
        # Combos
        combo_css = f"""
            QComboBox {{
                background-color: {p['surface0']};
                color: {p['text']};
                border: 1px solid {p['surface1']};
                border-radius: 4px;
                padding: 5px 10px;
            }}
            QComboBox:hover {{ border-color: {p['blue']}; }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{
                background-color: {p['surface0']};
                color: {p['text']};
                selection-background-color: {p['surface1']};
            }}
        """
        self.combo_flavor.setStyleSheet(combo_css)
        self.combo_style.setStyleSheet(combo_css)
        
        # Swatches
        colors = [("red", self.swatch_close), ("green", self.swatch_max), ("peach", self.swatch_min)]
        for key, sw in colors:
            sw.rect_frame.setStyleSheet(f"background-color: {p[key]}; border: none;")
            sw.name_lbl.setStyleSheet(sub)
        
        # Path
        aurorae = REPO_ROOT / "Resources" / "Aurorae" / f"Catppuccin{self.flavor}-{self.style}"
        if aurorae.exists():
            self.path_info.setText(f"✓ SVGs: {aurorae.relative_to(REPO_ROOT)}/")
            self.path_info.setStyleSheet(f"color: {p['green']}; font-size: 10px;")
        else:
            self.path_info.setText(f"✗ Not found: {aurorae}")
            self.path_info.setStyleSheet(f"color: {p['red']}; font-size: 10px;")


def main():
    print(f"Catppuccin Theme Preview")
    print(f"Repository: {REPO_ROOT}")
    print(f"PyQt6: {PYQT6}")
    print()
    
    app = QApplication(sys.argv)
    win = ThemeWindow()
    win.show()
    sys.exit(app.exec() if PYQT6 else app.exec_())


if __name__ == "__main__":
    main()
