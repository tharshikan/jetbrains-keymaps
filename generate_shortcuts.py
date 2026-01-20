import xml.etree.ElementTree as ET
import sys
import os

# Configuration
KEYMAP_FILE = "/Users/sanmugt/personal-configs/jetbrains-keymaps/webstorm/macOS copy.xml"
OUTPUT_FILE = "/Users/sanmugt/personal-configs/jetbrains-keymaps/WEBSTORM_SHORTCUTS.md"
OTHER_KEYMAPS_DIR = "/Users/sanmugt/personal-configs/jetbrains-keymaps/webstorm/"

# XML Key to Layout Key mapping
# This maps the internal XML key name to the Key Character found on the user's diagram
KEY_MAPPING = {
    "equals": "=", 
    "1": "1", "2": "2", "3": "3", "4": "4", "5": "5",
    "6": "6", "7": "7", "8": "8", "9": "9", "0": "0", 
    "open_bracket": "[", "close_bracket": "]",
    "tab": "TAB",
    "q": "Q", "p": "P", "u": "U", "y": "Y", "semicolon": ";",
    "k": "K", "f": "F", "l": "L", "r": "R", "b": "B", "back_slash": "\\",
    "escape": "ESC",
    "a": "A", "o": "O", "e": "E", "i": "I", "g": "G",
    "d": "D", "h": "H", "t": "T", "n": "N", "s": "S",
    "x": "X", "j": "J", "comma": ",", "period": ".", "quote": "'",
    "c": "C", "m": "M", "v": "V", "w": "W",
    "z": "Z", # Mentioned in row 5
    "left": "←", "right": "→", "up": "↑", "down": "↓",
    "minus": "-", # User diagram doesn't explicitly show minus in the main block, but often it's somewhere.
    "slash": "/", # not in main block
}

def format_action_name(action_id):
    if not action_id:
        return ""
    # Simplify common prefixes
    name = action_id
    replacements = {
        "Activate": "",
        "ToolWindow": "",
        "Editor": "",
        "Console": "",
        "Terminal": "",
        "Goto": "Go",
        "View": "",
        "Project": "Proj",
        "Structure": "Struct",
        "Bookmarks": "BkMk",
        "Favorites": "Favs",
        "Refactorings": "Refac",
        "QuickListPopupAction": "QList",
        "ShowIntentionActions": "Intent",
        "ShowPopupMenu": "PopUp",
        "Resize": "Rsz",
        "Duplicate": "Dup",
        "Word": "Wrd",
        "Delete": "Del",
        "Backspace": "BkSpc",
        "Forward": "Fwd",
        "Previous": "Prev",
        "Next": "Next",
        "Notebook": "NB",
        "Jupyter": "Jup",
        "Cell": "",
        "CommandModeAction": "",
    }
    
    # Strip dots
    if "." in name and " " not in name:
        name = name.split(".")[-1]
        
    for k, v in replacements.items():
        name = name.replace(k, v)
        
    # Formatting camel case to space? No space is tight.
    # Just truncate center if too long
    if len(name) > 8:
        return name[:8]
    return name

def parse_keymap(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    shortcuts = {}
    
    for action in root.findall('action'):
        action_id = action.get('id')
        for kbs in action.findall('keyboard-shortcut'):
            first = kbs.get('first-keystroke')
            if first:
                # Key format: "shift meta s"
                parts = first.split()
                key = parts[-1] 
                modifiers = tuple(sorted(parts[:-1]))
                
                if modifiers not in shortcuts:
                    shortcuts[modifiers] = {}
                
                # Check if we already have an entry, maybe prefer one?
                # We overwrite for now
                shortcuts[modifiers][key] = action_id
                
    return shortcuts

def render_layout(title, shortcuts_map, modifier_key):
    # modifier_key is a tuple like ('meta',) or ('shift', 'meta')
    
    # Get the specific map for this modifier
    actions = shortcuts_map.get(modifier_key, {})
    
    # Helper to get formatted action for a layout key
    def get_act(xml_key, key_label):
        # xml_key is the key in the XML (e.g. "s", "comma")
        # key_label is what we show if no action (e.g. "S", ","")
        
        act = actions.get(xml_key)
        if act:
            return format_action_name(act)
        return key_label

    # We need to construct the lines using format strings
    # Keys correspond to the user's diagram positions
    
    # Row 1 L
    k_eq = get_act("equals", "=")
    k_1 = get_act("1", "1")
    k_2 = get_act("2", "2")
    k_3 = get_act("3", "3")
    k_4 = get_act("4", "4")
    k_5 = get_act("5", "5")
    
    # Row 1 R
    k_6 = get_act("6", "6")
    k_7 = get_act("7", "7")
    k_8 = get_act("8", "8")
    k_9 = get_act("9", "9")
    k_0 = get_act("0", "0")
    k_lb = get_act("open_bracket", "[")

    # Row 2 L
    k_q = get_act("q", "Q")
    k_p = get_act("p", "P")
    k_u = get_act("u", "U")
    k_y = get_act("y", "Y")
    k_sc = get_act("semicolon", ";")
    
    # Row 2 R
    k_k = get_act("k", "K")
    k_f = get_act("f", "F")
    k_l = get_act("l", "L")
    k_r = get_act("r", "R")
    k_b = get_act("b", "B")
    k_bs = get_act("back_slash", "\\")

    # Row 3 L
    k_a = get_act("a", "A")
    k_o = get_act("o", "O")
    k_e = get_act("e", "E")
    k_i = get_act("i", "I")
    k_g = get_act("g", "G")
    
    # Row 3 R
    k_d = get_act("d", "D")
    k_h = get_act("h", "H")
    k_t = get_act("t", "T")
    k_n = get_act("n", "N")
    k_s = get_act("s", "S")
    
    # Row 4 L
    k_x = get_act("x", "X")
    k_j = get_act("j", "J")
    k_com = get_act("comma", ",")
    k_ueq = get_act("equals", "=") # User diagram has = here?
    k_quo = get_act("quote", "'")
    
    # Row 4 R
    k_c = get_act("c", "C")
    k_m = get_act("m", "M")
    k_v = get_act("v", "V")
    k_w = get_act("w", "W")
    k_dot = get_act("period", ".")
    
    # Row 5 (Thumbs/Bottom) - simplified for main block
    k_z = get_act("z", "Z") # L5
    k_rb = get_act("close_bracket", "]") # R5
    k_lf = get_act("left", "←")
    k_rt = get_act("right", "→")
    k_up = get_act("up", "↑")
    k_dn = get_act("down", "↓")

    diagram = f"""
## {title}

```
┌────────┬────────┬────────┬────────┬────────┬────────┬────────┐                                       ┌────────┬────────┬────────┬────────┬────────┬────────┬────────┐
│ {k_eq:^6} │ {k_1:^6} │ {k_2:^6} │ {k_3:^6} │ {k_4:^6} │ {k_5:^6} │ SL(1)  │                                       │ MO(3)  │ {k_6:^6} │ {k_7:^6} │ {k_8:^6} │ {k_9:^6} │ {k_0:^6} │ {k_lb:^6} │
├────────┼────────┼────────┼────────┼────────┼────────┼────────┤                                       ├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│  TAB   │ {k_q:^6} │ {k_p:^6} │ {k_u:^6} │ {k_y:^6} │ {k_sc:^6} │        │                                       │        │ {k_k:^6} │ {k_f:^6} │ {k_l:^6} │ {k_r:^6} │ {k_b:^6} │ {k_bs:^6} │
├────────┼────────┼────────┼────────┼────────┼────────┤        │                                       │        ├────────┼────────┼────────┼────────┼────────┼────────┤
│  ESC   │ {k_a:^6} │ {k_o:^6} │ {k_e:^6} │ {k_i:^6} │ {k_g:^6} │        │                                       │        │ {k_d:^6} │ {k_h:^6} │ {k_t:^6} │ {k_n:^6} │ {k_s:^6} │ SL(1)  │
├────────┼────────┼────────┼────────┼────────┼────────┴────────┤                                       ├────────┴────────┼────────┼────────┼────────┼────────┼────────┤
│ SHIFT  │ {k_x:^6} │ {k_j:^6} │ {k_com:^6} │ {k_ueq:^6} │ {k_quo:^6}       │                                       │        {k_c:^6} │ {k_m:^6} │ {k_v:^6} │ {k_w:^6} │ {k_dot:^6} │ SHIFT  │
└─┬──────┼────────┼────────┼────────┼────────┴─────────────┘                                       └─────────────┴────────┼────────┼────────┼────────┼────────┴┐
  │MO(2) │ {k_x:^6} │ {k_z:^6} │ {k_lf:^6} │ {k_rt:^6}                                                                          │ {k_up:^6} │ {k_dn:^6} │ {k_rb:^6} │MO(5)│MO(2) │
  └──────┴────────┴────────┴────────┘                                                                            └────────┴────────┴────────┴───────┘
```
"""
    return diagram

def main():
    if not os.path.exists(KEYMAP_FILE):
        print(f"Error: {KEYMAP_FILE} not found.")
        return

    shortcuts = parse_keymap(KEYMAP_FILE)
    
    # Defaults for Mac OS X 10.5+ parent keymap (Common/Essential only)
    # These fill in the gaps where the user hasn't overridden the key
    defaults = {
         ('meta',): {
             'e': 'RecentFiles',
             'c': 'Copy',
             'v': 'Paste',
             'z': 'Undo',
             'a': 'SelectAll',
             'f': 'Find',
             'g': 'FindNext',
             'comma': 'Preferences',
             'semicolon': 'ProjectStructure', # Often Cmd+;
             'slash': 'CommentByLineComment',
             'open_bracket': 'Back', # Default Mac
             'close_bracket': 'Forward', # Default Mac
         },
         ('shift', 'meta'): {
             'z': 'Redo',
             'f': 'FindInPath',
             'r': 'ReplaceInPath',
             'a': 'FindAction',
             'enter': 'CompleteCurrentStatement',
             'back_space': 'DeleteLine',
         }
    }
    
    # Merge defaults into shortcuts (only if not present)
    for mods, mod_map in defaults.items():
        if sorted(mods) not in [sorted(k) for k in shortcuts]:
             shortcuts[mods] = {}
        
        # We need to find the canonical key for the modifier tuple
        canonical_mods = None
        for m in shortcuts:
            if sorted(m) == sorted(mods):
                canonical_mods = m
                break
        if not canonical_mods:
             canonical_mods = mods
             shortcuts[canonical_mods] = {}
             
        for k, act in mod_map.items():
            if k not in shortcuts[canonical_mods]:
                shortcuts[canonical_mods][k] = act

    # Generation
    content = []
    content.append("# WebStorm Shortcuts\n")
    content.append(f"**Source:** `{os.path.basename(KEYMAP_FILE)}`")
    
    # 1. Cmd
    content.append(render_layout("Layer: Command (⌘)", shortcuts, ('meta',)))
    
    # 2. Opt
    content.append(render_layout("Layer: Option (⌥)", shortcuts, ('alt',)))
    
    # 3. Cmd+Shift
    content.append(render_layout("Layer: Command + Shift (⌘⇧)", shortcuts, ('meta', 'shift')))
    
    # All Shortcuts Table
    content.append("\n## All Shortcuts Reference")
    content.append("| Keys | Action |")
    content.append("| :--- | :--- |")
    
    # Flatten and sort
    all_list = []
    for mods, keys_map in shortcuts.items():
        mod_str = " ".join(mods)
        for k, act in keys_map.items():
            all_list.append((mod_str + " " + k, act))
            
    all_list.sort()
    
    for k, act in all_list:
        content.append(f"| `{k}` | {act} |")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(content))
        
    print(f"Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
