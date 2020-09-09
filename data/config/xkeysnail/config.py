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


# ext and add_bindings are convenience funtions to use multiple keymaps that use a group with the same modifier key (in vanilla xkeysnails, only one keymap can define a group for a modifier)
def ext(*named_bindings):
    binding_origin = {}
    r = {}
    desc = "<"
    for nb in named_bindings:
        b, n = nb
        desc += (", " if desc != "<" else "") + n
        for k in b:
            if k in r:
                if type(r[k]) != type(b[k]):
                    print(f"key binding {k} cannot be overridden "
                          f"from type {type(r[k])} ({binding_origin[k]}) "
                          f"to {type(b[k])} ({n}) with different type")
                elif isinstance(r[k], dict):  # override group key
                    overridden_keys = [x for x in r[k] if x in b[k]]
                    for x in overridden_keys:
                        print(f"key binding {k} {x} is overridden "
                              f"from {[str(y) for y in r[k][x]] if isinstance(r[k][x], list) else r[k][x]} ({binding_origin[k][x]}) "
                              f"to {[str(y) for y in b[k][x]] if isinstance(b[k][x], list) else b[k][x]} ({n})")
                    r[k] = {**r[k], **b[k]}
                    # x = {x:n for x in b[k]}
                    # print('b')
                    # print(x)
                    # print('binding_origin')
                    # print(binding_origin[k])
                    binding_origin[k] = {**binding_origin[k], **{x:n for x in b[k]}}
                else:  # override key combo
                    print(f"key binding {k} is overridden "
                          f"from {[str(y) for y in r[k]] if isinstance(r[k], list) else r[k]} ({binding_origin[k]}) "
                          f"to {[str(y) for y in b[k]] if isinstance(b[k], list) else b[k]} ({n})")
                    r[k] = b[k]
                    binding_origin[k] = n
            else:
                r[k] = b[k]
                if isinstance(b[k], dict):
                    binding_origin[k] = {x:n for x in b[k]}
                else:
                    binding_origin[k] = n
    return (r, desc+">")


def add_bindings(cond, description, *bindings):
    print(f"Adding bindings for: {description}")
    binding, binding_description = ext(*bindings)
    define_keymap(cond,
                  binding,
                  description+" "+binding_description)


common_browser = ({
    # Ctrl+Alt+j/k to switch next/previous tab
    K("C-M-j"): K("C-TAB"),
    K("C-M-k"): K("C-Shift-TAB"),
    # Type C-j to focus to the content
    K("C-j"): K("C-f6"),
    # very naive "Edit in editor" feature (just an example)
    # K("C-o"): [K("C-a"), K("C-c"), launch(["gedit"]), sleep(0.5), K("C-v")],
    # jump to page in pdf viewer
    K("M-g"): {
        K("M-g"): K("C-M-g"),
        # the following is invoked if the alt key (M-) is not released after pressing g
        K("g"): K("C-M-g"),
        # cancel
        K("C-g"): pass_through_key,
    }},
    "common browser keys")

# Keybindings for okular
okular = ({
    # Go to line
    K("M-g"): {K("M-g"): K("C-g")},
    K("C-x"): {
        # C-x C-s (save)
        K("C-s"): K("C-Shift-S"),
        # cancel
        K("C-g"): pass_through_key,
    }},
    "okular go-to page and save")

jupyter_webbrowser = ({
    # comment line or region
    K("C-x"): {
        K("C-semicolon"): K("C-slash"),
        # # cancel
        K("C-g"): pass_through_key,
    },
    K("C-c"): {
        K("M-d"): [K("home"), K("left"), K("Shift-right"), K("Shift-end"), K("C-c"), K("end"), K("C-v"), K("home"), K("left"), K("C-slash")],
        # cancel
        K("C-g"): pass_through_key,
    }},
    "jupyter web interface")

save = ({
    K("C-x"): {
        # C-x C-s (save)
        K("C-s"): K("C-s"),
        # # cancel
        K("C-g"): pass_through_key,
    }},
    "Emacs-like save")

text_navigation = ({
    # Cursor
    K("C-b"): with_mark(K("left")),
    K("C-f"): with_mark(K("right")),
    K("C-p"): with_mark(K("up")),
    K("C-n"): with_mark(K("down")),
    # Forward/Backward word
    K("M-b"): with_mark(K("C-left")),
    K("M-f"): with_mark(K("C-right")),
    },
    "Emacs-like text navigation")

page_navigation = ({
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
    },
    "Emacs-like page navigation")

search = ({
    # Search
    # K("C-s"): K("F3"),
    # K("C-r"): K("Shift-F3"),
    K("C-s"): K("C-f"),
    K("C-r"): K("Shift-F3"),
    K("M-Shift-key_5"): K("C-h"),
    },
    "Emacs-like search")

delete = ({
    # Delete
    K("C-d"): [K("delete"), set_mark(False)],
    K("M-d"): [K("C-delete"), set_mark(False)],
    K("M-backspace"): K("C-backspace"),
    # Kill line
    K("C-k"): [K("Shift-end"), K("C-x"), set_mark(False)],
    # Kill whole line
    K("C-Shift-backspace"): [K("home"), K("Shift-end"), K("Shift-right"), K("C-x")],
    },
    "Emacs-like deletion")


misc = ({
    K("C-h"): with_mark(K("backspace")),
    # Newline
    K("C-m"): K("enter"),
    # K("C-j"): K("enter"),
    # K("C-o"): [K("enter"), K("left")],
    # Copy
    K("C-w"): [K("C-x"), set_mark(False)],
    K("M-w"): [K("C-c"), set_mark(False)],
    K("C-y"): [K("C-v"), set_mark(False)],
    # Undo
    K("C-slash"): [K("C-z"), set_mark(False)],
    K("C-Shift-ro"): K("C-z"),
    # Mark
    K("C-space"): set_mark(True),
    K("C-M-space"): with_or_set_mark(K("C-right")),
    # Cancel
    K("C-g"): [set_mark(False), K("esc")],
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
    }},
    "Emacs-like misc keys")

default_bindings = [save, text_navigation, page_navigation, delete, search, misc]

add_bindings(
    re.compile("Google-chrome"),
    "Chrome",
    *(default_bindings + [common_browser, jupyter_webbrowser])
)

add_bindings(
    re.compile("Firefox"),
    "Firefox",
    *(default_bindings + [common_browser, jupyter_webbrowser])
)

add_bindings(
    re.compile("okular"),
    "Okular",
    okular, text_navigation, page_navigation, delete, search, misc
)

add_bindings(
    re.compile("Evince"),
    "Evince",
    save, text_navigation, page_navigation, delete, misc
)

add_bindings(
    re.compile("Thunderbird"),
    "Thunderbird",
    text_navigation, page_navigation, delete
)

add_bindings(
    lambda wm_class: wm_class
    not in (
        "Emacs",
        "URxvt",
        "Gnome-terminal",
        "Firefox",
        "Google-chrome",
        "okular",
        "Evince",
        "Thunderbird",
    ),
    "Non customized applications",
    *default_bindings
)
