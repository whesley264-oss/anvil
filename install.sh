#!/bin/bash
# ANVIL Installer v1.5 - Modular Installation
# Usage: curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash
# Or with mode: curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash -s -- --mode light

set -e

INSTALL_DIR="$HOME/.anvil"
REPO_URL="https://github.com/whesley264-oss/anvil.git"
MODE="normal"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --mode=*)
            MODE="${1#*=}"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}"
echo "╔══════════════════════════════════════════╗"
echo "║         ANVIL Installer v1.5              ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${CYAN}ℹ Installation mode: ${MODE}${NC}"
echo ""

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
    git config pull.rebase false
    git config fetch.prune true
    git reset --hard HEAD
    git clean -fd
    git fetch --all
    git reset --hard origin/main
else
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

if [ ! -f "$INSTALL_DIR/anvil_cli.py" ]; then
    echo -e "${RED}✗ Download failed${NC}"
    exit 1
fi

chmod +x "$INSTALL_DIR/anvil_cli.py"

# Install based on mode
case $MODE in
    light)
        echo -e "${CYAN}ℹ Installing ANVIL Light (~10MB)${NC}"
        pip install -e . --no-console-scripts 2>/dev/null || \
        pip3 install -e . --no-console-scripts 2>/dev/null || \
        pip install . 2>/dev/null || \
        pip3 install . 2>/dev/null || true
        echo -e "${GREEN}✓ ANVIL Light installed!${NC}"
        ;;
    
    normal)
        echo -e "${CYAN}ℹ Installing ANVIL Normal (~50MB)${NC}"
        pip install -e . --no-console-scripts 2>/dev/null || \
        pip3 install -e . --no-console-scripts 2>/dev/null || \
        pip install . 2>/dev/null || \
        pip3 install . 2>/dev/null || true
        echo -e "${GREEN}✓ ANVIL Normal installed!${NC}"
        ;;
    
    full)
        echo -e "${CYAN}ℹ Installing ANVIL Full (~2GB)${NC}"
        pip install -e . --no-console-scripts 2>/dev/null || \
        pip3 install -e . --no-console-scripts 2>/dev/null || \
        pip install . 2>/dev/null || \
        pip3 install . 2>/dev/null || true
        
        # Install Android SDK for full mode
        if [ "$PLATFORM" = "termux" ]; then
            echo -e "${CYAN}ℹ Installing Android SDK...${NC}"
            SDK_DIR="$HOME/android-sdk"
            mkdir -p "$SDK_DIR"
            
            CMDLINE_URL="https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
            echo -e "${CYAN}ℹ Downloading Android command-line tools...${NC}"
            
            cd "$SDK_DIR"
            curl -L -o cmdline-tools.zip "$CMDLINE_URL"
            unzip -q cmdline-tools.zip
            rm cmdline-tools.zip
            
            mkdir -p cmdline-tools/latest
            mv cmdline-tools/bin cmdline-tools/latest/ 2>/dev/null || true
            mv cmdline-tools/lib cmdline-tools/latest/ 2>/dev/null || true
            
            yes | "$SDK_DIR/cmdline-tools/latest/bin/sdkmanager" --licenses 2>/dev/null || true
            "$SDK_DIR/cmdline-tools/latest/bin/sdkmanager" "platform-tools" "platforms;android-34" "build-tools;34.0.0" 2>/dev/null || true
            
            echo -e "${GREEN}✓ Android SDK installed!${NC}"
        fi
        ;;
    
    *)
        echo -e "${YELLOW}⚠ Unknown mode: $MODE, using normal${NC}"
        pip install -e . --no-console-scripts 2>/dev/null || true
        ;;
esac

# Create launcher
echo -e "${CYAN}ℹ Creating launcher...${NC}"
rm -f "$BIN_DIR/anvil" 2>/dev/null || true

cat > "$BIN_DIR/anvil" << 'LAUNCHER'
#!/bin/bash
export ANVIL_HOME="$HOME/.anvil"
export PYTHONPATH="$ANVIL_HOME:$PYTHONPATH"

if [ -d "$PREFIX/lib/jvm/java-17-openjdk" ]; then
    export JAVA_HOME="$PREFIX/lib/jvm/java-17-openjdk"
    export PATH="$JAVA_HOME/bin:$PATH"
fi

if [ -d "$HOME/android-sdk" ]; then
    export ANDROID_HOME="$HOME/android-sdk"
    export ANDROID_SDK_ROOT="$HOME/android-sdk"
    export PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools"
fi

exec python3 "$ANVIL_HOME/anvil_cli.py" "$@"
LAUNCHER

chmod +x "$BIN_DIR/anvil"

VERSION=$(python3 "$INSTALL_DIR/anvil_cli.py" --version 2>&1 | grep -oP '[\d.]+' | head -1 || echo "unknown")
if [ "$VERSION" != "unknown" ]; then
    echo -e "${GREEN}✓ ANVIL installed successfully!${NC}"
    echo -e "${BOLD}Version: ${VERSION}${NC}"
else
    echo -e "${YELLOW}⚠ ANVIL installed but version check failed${NC}"
fi

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
    fi
fi

echo ""
echo -e "${BOLD}Installation modes:${NC}"
echo "  --mode light   - Minimal (~10MB)"
echo "  --mode normal  - Standard (~50MB)"  
echo "  --mode full    - Complete (~2GB)"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo "  1. Run: ${CYAN}zsh${NC}   (only on Termux)"
echo "  2. Run: ${CYAN}anvil --help${NC}   (show commands)"
echo "  3. Run: ${CYAN}anvil init${NC}      (create project)"
echo ""
echo -e "${CYAN}Quick commands:${NC}"
echo "  anvil lang --set pt    - Change to Portuguese"
echo "  anvil doctor           - Check system"
echo "  anvil light            - Use lightweight build"
echo "  anvil quick-build      - Fast APK build"