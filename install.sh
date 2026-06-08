#!/bin/bash
# ANVIL Installer v1.4
# Usage: curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash

set -e

INSTALL_DIR="$HOME/.anvil"
REPO_URL="https://github.com/whesley264-oss/anvil.git"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}"
echo "╔══════════════════════════════════════════╗"
echo "║         ANVIL Installer v1.4              ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# Detect platform
PLATFORM="unknown"
if [ -n "$TERMUX_APP" ] || [ -d "$PREFIX" ] || [ -d "$HOME/.termux" ]; then
    PLATFORM="termux"
    BIN_DIR="$PREFIX/bin"
elif [ "$(uname)" = "Darwin" ]; then
    PLATFORM="macos"
    BIN_DIR="/usr/local/bin"
elif grep -qi microsoft /proc/version 2>/dev/null; then
    PLATFORM="wsl"
elif [ "$(uname)" = "Linux" ]; then
    PLATFORM="linux"
    BIN_DIR="$HOME/.local/bin"
fi

echo -e "${CYAN}ℹ Detected platform: ${PLATFORM}${NC}"

# Check for internet
if ! curl -s --max-time 5 https://api.github.com > /dev/null 2>&1; then
    echo -e "${RED}✗ No internet connection${NC}"
    exit 1
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Clone or update
echo -e "${CYAN}ℹ Downloading ANVIL...${NC}"

if [ -d "$INSTALL_DIR/.git" ]; then
    echo -e "${CYAN}ℹ Updating existing installation...${NC}"
    cd "$INSTALL_DIR"
    
    # Configure git to handle divergent branches
    git config pull.rebase false
    git config fetch.prune true
    
    # Handle local changes - reset hard to get clean state
    git reset --hard HEAD
    git clean -fd
    git fetch --all
    git reset --hard origin/main
else
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Check if clone was successful
if [ ! -f "$INSTALL_DIR/anvil_cli.py" ]; then
    echo -e "${RED}✗ Download failed${NC}"
    exit 1
fi

# Make executable
chmod +x "$INSTALL_DIR/anvil_cli.py"

# Install Python deps WITHOUT console scripts (to prevent overwrite)
echo -e "${CYAN}ℹ Installing Python dependencies...${NC}"
cd "$INSTALL_DIR"

# Install without creating console scripts that would overwrite our launcher
pip install -e . --no-console-scripts 2>/dev/null || \
pip3 install -e . --no-console-scripts 2>/dev/null || \
pip install -e . --skip-scripts 2>/dev/null || \
pip3 install -e . --skip-scripts 2>/dev/null || \
pip install . 2>/dev/null || \
pip3 install . 2>/dev/null || \
true

# Create wrapper script (solves module import issues)
echo -e "${CYAN}ℹ Creating launcher...${NC}"

# Remove old file/symlink if exists
rm -f "$BIN_DIR/anvil" 2>/dev/null || true

# Create a bash launcher script
cat > "$BIN_DIR/anvil" << 'LAUNCHER'
#!/bin/bash
# ANVIL Launcher - Sets up Python path correctly
export ANVIL_HOME="$HOME/.anvil"
export PYTHONPATH="$ANVIL_HOME:$PYTHONPATH"
exec python3 "$ANVIL_HOME/anvil_cli.py" "$@"
LAUNCHER

chmod +x "$BIN_DIR/anvil"

# Verify launcher
if [ -f "$BIN_DIR/anvil" ]; then
    echo -e "${GREEN}✓ Launcher created: $BIN_DIR/anvil${NC}"
else
    echo -e "${RED}✗ Failed to create launcher${NC}"
    exit 1
fi

# Verify installation - silent check
echo ""
echo -e "${CYAN}ℹ Verifying installation...${NC}"

# Test the launcher directly (silent)
VERSION=$(python3 "$INSTALL_DIR/anvil_cli.py" --version 2>&1 | grep -oP '[\d.]+' | head -1 || echo "unknown")

if [ "$VERSION" != "unknown" ]; then
    echo -e "${GREEN}✓ ANVIL installed successfully!${NC}"
    echo -e "${BOLD}Version: ${VERSION}${NC}"
else
    echo -e "${YELLOW}⚠ ANVIL installed but version check failed${NC}"
fi

# Auto-add PATH to shell config
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "$BIN_DIR" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# ANVIL" >> "$SHELL_RC"
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
        echo -e "${CYAN}ℹ Added PATH to $SHELL_RC${NC}"
    fi
fi

echo ""
echo -e "${BOLD}Next steps:${NC}"
echo ""
echo "  1. Run: ${CYAN}zsh${NC}   (only on Termux - switches to ZSH shell)"
echo "  2. Run: ${CYAN}anvil --help${NC}   (show all commands)"
echo "  3. Run: ${CYAN}anvil init${NC}      (create new project)"
echo ""
echo -e "${YELLOW}⚠ On Termux: you MUST use ZSH shell!${NC}"
echo -e "${YELLOW}   Type 'zsh' and press Enter to switch${NC}"
echo ""
echo -e "${CYAN}Quick commands:${NC}"
echo "  anvil lang --set pt    - Change to Portuguese"
echo "  anvil doctor           - Check system"
echo "  anvil inspect <url>     - Analyze website"
echo "  anvil run              - Start dev server"
echo ""