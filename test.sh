#!/bin/bash
# Catppuccin Theme Test Script
# Opens various KDE windows to test the current theme configuration

echo "=== Catppuccin Theme Tester ==="
echo ""
echo "This script opens KDE test windows to preview the current theme."
echo ""

# Check for required tools
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo "Warning: $1 not found"
        return 1
    fi
    return 0
}

# Test 1: Open KDE Window Decoration Settings (shows live preview)
test_window_decorations() {
    echo "[1/4] Opening Window Decoration Settings..."
    if check_tool kcmshell6; then
        kcmshell6 kcm_kwindecoration &
    elif check_tool kcmshell5; then
        kcmshell5 kcm_kwindecoration &
    else
        echo "  -> kcmshell not available"
    fi
}

# Test 2: Open Color Scheme Settings
test_color_scheme() {
    echo "[2/4] Opening Color Scheme Settings..."
    if check_tool kcmshell6; then
        kcmshell6 kcm_colors &
    elif check_tool kcmshell5; then
        kcmshell5 kcm_colors &
    else
        echo "  -> kcmshell not available"
    fi
}

# Test 3: Open a KDE dialog with various elements
test_kdialog() {
    echo "[3/4] Opening KDialog test windows..."
    if check_tool kdialog; then
        # Show a message box
        kdialog --title "Catppuccin Theme Test" \
                --msgbox "This is a test window to preview the Catppuccin theme.\n\nCheck the:\n• Window decoration (title bar buttons)\n• Window colors\n• Button styling" &
        
        # Show a menu/list dialog
        kdialog --title "Theme Element Test" \
                --menu "Select an option to test different UI elements:" \
                1 "Close Button (Red)" \
                2 "Minimize Button (Peach)" \
                3 "Maximize Button (Green)" \
                4 "Window Background" &
    else
        echo "  -> kdialog not available"
    fi
}

# Test 4: Open Konsole (terminal) to see color scheme
test_konsole() {
    echo "[4/4] Opening Konsole..."
    if check_tool konsole; then
        konsole --hold -e bash -c '
            echo "=== Catppuccin Theme Test ==="
            echo ""
            echo -e "\e[31m██ Red (Close)\e[0m"
            echo -e "\e[33m██ Peach/Yellow (Minimize)\e[0m"  
            echo -e "\e[32m██ Green (Maximize)\e[0m"
            echo ""
            echo "Press Enter to close..."
            read
        ' &
    else
        echo "  -> konsole not available"
    fi
}

# Test 5: Open Dolphin file manager
test_dolphin() {
    echo "[Bonus] Opening Dolphin file manager..."
    if check_tool dolphin; then
        dolphin --new-window . &
    fi
}

# Run all tests
echo "Opening test windows..."
echo ""

test_window_decorations
sleep 0.3
test_color_scheme
sleep 0.3
test_kdialog
sleep 0.3
test_konsole
sleep 0.3
test_dolphin

echo ""
echo "Done! Check the opened windows to see your theme."
echo ""
echo "Tips:"
echo "  - Look at the title bar buttons (should be horizontal rectangles)"
echo "  - Check the window colors match your selected flavor"
echo "  - Close button = Red, Minimize = Peach, Maximize = Green"
echo ""
echo "Press Enter to close all test windows..."
read

# Cleanup - close test windows
pkill -f "kcmshell.*kcm_kwindecoration" 2>/dev/null
pkill -f "kcmshell.*kcm_colors" 2>/dev/null
pkill -f "kdialog.*Catppuccin" 2>/dev/null
