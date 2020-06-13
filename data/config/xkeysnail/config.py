# -*- coding: utf-8 -*-

import re
from xkeysnail.transform import (
    define_keymap,
    define_conditional_modmap,
    define_multipurpose_modmap,
    Key,
    K,
    with_mark,
    set_mark,
    with_or_set_mark,
    launch,
    sleep,
    escape_next_key,
    pass_through_key,
)

# [Global modemap] Change modifier keys as in xmodmap
# define_modmap({
#     Key.CAPSLOCK: Key.LEFT_CTRL
# })

# [Conditional modmap] Change modifier keys in certain applications
define_conditional_modmap(re.compile(r"Emacs"), {Key.RIGHT_CTRL: Key.ESC})

# [Multipurpose modmap] Give a key two meanings. A normal key when pressed and
# released, and a modifier key when held down with another key. See Xcape,
# Carabiner and caps2esc for ideas and concept.
define_multipurpose_modmap(
    # Enter is enter when pressed and released. Control when held down.
    {Key.ENTER: [Key.ENTER, Key.RIGHT_CTRL]}
    # Capslock is escape when pressed and released. Control when held down.
    # {Key.CAPSLOCK: [Key.ESC, Key.LEFT_CTRL]
    # To use this example, you can't remap capslock with define_modmap.
)


# Keybindings for Firefox/Chrome
define_keymap(
    re.compile("Firefox|Google-chrome"),
    {
        # Ctrl+Alt+j/k to switch next/previous tab
        K("C-M-j"): K("C-TAB"),
        K("C-M-k"): K("C-Shift-TAB"),
        # Type C-j to focus to the content
        K("C-j"): K("C-f6"),
        # very naive "Edit in editor" feature (just an example)
        K("C-o"): [K("C-a"), K("C-c"), launch(["gedit"]), sleep(0.5), K("C-v")],
        # jump to page in pdf viewer
        K("M-g"): {
            K("M-g"): K("C-M-g"),
            # the following is invoked if the alt key (M-) is not released after pressing g
            K("g"): K("C-M-g"),
            # cancel
            K("C-g"): pass_through_key,
        },
    },
    "Firefox and Chrome",
)

# # Keybindings for Zeal https://github.com/zealdocs/zeal/
# define_keymap(re.compile("Zeal"), {
#     # Ctrl+s to focus search area
#     K("C-s"): K("C-k"),
# }, "Zeal")

# Keybindings for okular
define_keymap(
    re.compile("okular"),
    {
        # Go to line
        K("M-g"): {K("M-g"): K("C-g")},
        K("C-x"): {
            # C-x C-s (save)
            K("C-s"): K("C-Shift-S"),
            # cancel
            K("C-g"): pass_through_key,
        }
    },
    "okular go-to page and save",
)

# Keybindings for firefox+jupyter
define_keymap(
    re.compile("Firefox"),
    {
        # comment line or region
        K("C-x"): {
            K("C-semicolon"): K("C-slash"),
            # cancel
            K("C-g"): pass_through_key,
        },
        K("C-c"): {
            K("M-d"): [K("home"), K("left"), K("Shift-right"), K("Shift-end"), K("C-c"), K("end"), K("C-v"), K("home"), K("left"), K("C-slash")],
            # cancel
            K("C-g"): pass_through_key,
        }
    },
    "Firefox + jupyter comment line",
)

# Emacs-like save
define_keymap(
    lambda wm_class: wm_class not in ("Emacs", "URxvt", "Gnome-terminal", "okular"),
    {
        K("C-x"): {
            # C-x C-s (save)
            K("C-s"): K("C-s"),
            # cancel
            K("C-g"): pass_through_key,
        },
    },
    "Emacs-like save",
)

# Emacs-like navigation
define_keymap(
    lambda wm_class: wm_class not in ("Emacs", "URxvt", "Gnome-terminal", "Evince"),
    {
        # Cursor
        K("C-b"): with_mark(K("left")),
        K("C-f"): with_mark(K("right")),
        K("C-p"): with_mark(K("up")),
        K("C-n"): with_mark(K("down")),
    },
    "Emacs-like navigation",
)

# Emacs-like search
# Emacs-like keybindings in non-Emacs applications
define_keymap(
    lambda wm_class: wm_class not in ("Emacs", "URxvt", "Gnome-terminal", "Evince"),
    {
        # Search
        # K("C-s"): K("F3"),
        # K("C-r"): K("Shift-F3"),
        K("C-s"): K("C-f"),
        K("C-r"): K("Shift-F3"),
        K("M-Shift-key_5"): K("C-h"),
    },
    "Emacs-like search",
)

# Emacs-like others
define_keymap(
    lambda wm_class: wm_class not in ("Emacs", "URxvt", "Gnome-terminal"),
    {
        K("C-h"): with_mark(K("backspace")),
        # Forward/Backward word
        K("M-b"): with_mark(K("C-left")),
        K("M-f"): with_mark(K("C-right")),
        # Beginning/End of line
        K("C-a"): with_mark(K("home")),
        K("C-e"): with_mark(K("end")),
        # Page up/down
        K("M-v"): with_mark(K("page_up")),
        K("C-v"): with_mark(K("page_down")),
        # Beginning/End of file
        K("M-Shift-comma"): with_mark(K("C-home")),
        K("M-Shift-dot"): with_mark(K("C-end")),
        K("M-KEY_102ND"): with_mark(K("C-home")),
        K("M-Shift-KEY_102ND"): with_mark(K("C-end")),
        # Newline
        K("C-m"): K("enter"),
        K("C-j"): K("enter"),
        K("C-o"): [K("enter"), K("left")],
        # Copy
        K("C-w"): [K("C-x"), set_mark(False)],
        K("M-w"): [K("C-c"), set_mark(False)],
        K("C-y"): [K("C-v"), set_mark(False)],
        # Delete
        K("C-d"): [K("delete"), set_mark(False)],
        K("M-d"): [K("C-delete"), set_mark(False)],
        # Kill line
        K("C-k"): [K("Shift-end"), K("C-x"), set_mark(False)],
        # Kill whole line
        K("C-Shift-backspace"): [K("home"), K("Shift-end"), K("Shift-right"), K("C-x")],
        # Undo
        K("C-slash"): [K("C-z"), set_mark(False)],
        K("C-Shift-ro"): K("C-z"),
        # Mark
        K("C-space"): set_mark(True),
        K("C-M-space"): with_or_set_mark(K("C-right")),
        # Cancel
        K("C-g"): [K("esc"), set_mark(False)],
        # Escape
        K("C-q"): escape_next_key,
        # C-x YYY
        K("C-x"): {
            # C-x h (select all)
            K("h"): [K("C-home"), K("C-a"), set_mark(True)],
            # C-x C-f (open)
            K("C-f"): K("C-o"),
            # C-x k (kill tab)
            K("k"): K("C-f4"),
            # C-x C-c (exit)
            K("C-c"): K("C-q"),
            # cancel
            K("C-g"): pass_through_key,
            # C-x u (undo)
            K("u"): [K("C-z"), set_mark(False)],
        },
        K("C-c"): {
            # print document
            K("p"): K("C-p"),
        },
    },
    "Emacs-like keys",
)
