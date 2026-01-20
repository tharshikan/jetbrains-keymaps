#!/bin/bash

# Configuration
REPO_ROOT="$HOME/personal-configs/jetbrains-keymaps"
BACKUP_DIR="$HOME/jetbrains-keymap-backups/$(date +%Y%m%d_%H%M%S)"

# IDE Mapping: "Repo_Folder_Name:System_Folder_Name"
# These versions match your screenshot (2025.3)
declare -a ide_mappings=(
    "webstorm:WebStorm2025.3"
    "intellij:IntelliJIdea2025.3"
    "pycharm:PyCharm2025.3"
)

echo "Starting setup..."
mkdir -p "$BACKUP_DIR"
echo "✅ Backup directory created at: $BACKUP_DIR"

for mapping in "${ide_mappings[@]}"; do
    repo_folder="${mapping%%:*}"
    system_folder_name="${mapping##*:}"
    
    repo_path="$REPO_ROOT/$repo_folder"
    system_path="$HOME/Library/Application Support/JetBrains/$system_folder_name/keymaps"

    echo "---------------------------------------------------"
    echo "Processing $system_folder_name..."

    # 1. Ensure the Repo subfolder exists
    mkdir -p "$repo_path"

    # 2. Check if the IDE folder exists
    if [ -d "$system_path" ]; then
        if [ -L "$system_path" ]; then
            echo "   ⚠️  $system_folder_name is already linked. Skipping."
            continue
        fi

        # 3. BACKUP: Copy current config to safe backup folder
        echo "   📦 Backing up existing keymaps..."
        cp -R "$system_path/" "$BACKUP_DIR/$system_folder_name/"

        # 4. MIGRATE: Move XMLs to Git repo (only if repo folder is empty)
        if [ -z "$(ls -A "$repo_path")" ]; then
             echo "   🚚 Moving existing XMLs to Git repo..."
             mv "$system_path/"*.xml "$repo_path/" 2>/dev/null
        fi

        # 5. REMOVE original folder
        rm -rf "$system_path"
    else
        echo "   Target directory didn't exist, creating parent structure..."
        mkdir -p "$(dirname "$system_path")"
    fi

    # 6. LINK
    ln -s "$repo_path" "$system_path"
    echo "   🔗 Symlink created!"
done

echo "---------------------------------------------------"
echo "🎉 Done! Backups saved in: $BACKUP_DIR"
