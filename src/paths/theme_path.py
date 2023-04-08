from pathlib import Path

DARK_THEME_NAME = "Forest-ttk-theme/forest-dark.tcl"
LIGHT_THEME_NAME = "Forest-ttk-theme/forest-light.tcl"

BASE_DIR = Path(__file__).parent.parent.parent

THEME_DARK = BASE_DIR.joinpath(DARK_THEME_NAME)
THEME_LIGHT = BASE_DIR.joinpath(LIGHT_THEME_NAME)

if __name__ == "__main__":
    print(THEME_DARK, THEME_LIGHT)
