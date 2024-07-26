#!/bin/bash
set -e

# Set up USER_BIN
USER_BIN="$HOME/.local/bin"

# GitHub repository information
REPO_OWNER="vsbuffalo"
REPO_NAME="vbtk"
BRANCH="main"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to set up USER_BIN
setup_user_bin() {
    if [ ! -d "$USER_BIN" ]; then
        mkdir -p "$USER_BIN"
        echo "Created $USER_BIN directory."
    fi
    if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
        echo "Adding $USER_BIN to PATH for this session."
        export PATH="$USER_BIN:$PATH"
        echo "To add it permanently, add the following line to your .bashrc or .bash_profile:"
        echo "export PATH=\"$USER_BIN:\$PATH\""
    fi
}

# Function to download a file from GitHub
download_file() {
    local file_path="$1"
    local url="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${BRANCH}/${file_path}"
    echo "Downloading $url..."
    curl -sSL "$url" -o "$(basename "$file_path")"
}

# Function to install a script
install_script() {
    local script="$1"
    local target="$USER_BIN/$(basename "${script%.*}")"

    if [ -f "$target" ] && [ "$OVERWRITE" != "true" ]; then
        echo "Error: $target already exists. Use --overwrite to replace it."
        return 1
    fi

    cp "$script" "$target"
    chmod +x "$target"
    echo "Installed $target"
}

# Main installation function
install_toolkit() {
    echo "Starting toolkit installation..."

    # Set up USER_BIN
    setup_user_bin

    # Check for required tools
    for cmd in curl cp chmod mktemp; do
        if ! command_exists $cmd; then
            echo "Error: $cmd is not installed. Please install it and try again."
            exit 1
        fi
    done

    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    echo "Working in temporary directory: $TEMP_DIR"
    cd "$TEMP_DIR"

    # Install scripts
    local scripts=(
        "python/stdin_rate.py"
        "python/snklog.py"
    )

    for script in "${scripts[@]}"; do
        echo "Downloading $script..."
        download_file "$script"
        if [ -f "$(basename "$script")" ]; then
            install_script "$(basename "$script")"
        else
            echo "Warning: Failed to download $script. Skipping."
        fi
    done

    # Clean up
    cd
    rm -rf "$TEMP_DIR"

    echo "Toolkit installation completed successfully!"
    echo "Make sure $USER_BIN is in your PATH."
}

# Parse command line arguments
OVERWRITE=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --overwrite)
            OVERWRITE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run the installation
install_toolkit
