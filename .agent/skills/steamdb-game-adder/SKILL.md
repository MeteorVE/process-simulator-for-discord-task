---
description: Search SteamDB for a game's executable and add it to the project's config.py
---

# SteamDB Game Adder

This skill allows you to quickly find the executable name for a game on SteamDB and add it to the `GAME_PATHS` list in `config.py`.

## Usage

When the user provides a game name (or an image of a game that you have identified), follow these steps:

1.  **Search SteamDB**:
    - Use the `search_web` tool with the query: `site:steamdb.info [game name] config`.
    - Look for a result that points to the **Configuration** page (URL ending in `/config/`). If not found directly, find the AppID page and navigate to `/config/`.

2.  **Extract Executable Name**:
    - Visit the SteamDB Configuration page using `read_url_content` (or `read_browser_page` if needed).
    - Look for the `Executable` field or `launch/0/executable` section.
    - Extract the executable filename (e.g., `game.exe`, `Binaries\Win64\game.exe`).
    - If the path is long (e.g., `Binaries/Win64/game.exe`), extract just the **filename** (e.g., `game.exe`) unless the user specifies otherwise. The `ProcessSimulator` usually expects the relative path like `.\game.exe`.

3.  **Update `config.py`**:
    - Read `c:\Users\MeteorV\Downloads\ProcessSimulator\config.py` to check existing entries.
    - Append the new executable to the `GAME_PATHS` list.
    - Format: `r".\filename.exe",` (using `r` string and `.\` prefix is recommended).
    - **Do not enable** the game by default (leave it in the list).
    - Use `multi_replace_file_content` or `replace_file_content` to insert the new line *inside* the `GAME_PATHS` list comprehension or definition.

## Example

**User Input**: "Add 'Wuthering Waves' to config"

1.  **Search**: `site:steamdb.info Wuthering Waves config` -> Finds `https://steamdb.info/app/3564740/config/`
2.  **Extract**: Page shows `Executable: Wuthering Waves.exe` (or `Launcher.exe`). Let's say found `wwm.exe`.
3.  **Update**:
    ```python
    # config.py
    GAME_PATHS = [
        r".\existing_game.exe",
        r".\wwm.exe", # Added
    ]
    ```
