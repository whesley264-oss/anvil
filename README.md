# 🔨 ANVIL - Transform Websites into Android APKs

```
    _   _  _     _  ___  _      
   / \ | \ | || |   | ||_ _|| |     
  / _ \|  \| || |   | | | | | |     
 / ___ \ |\  | \ \ / /  | | | |___  
/_/   \_\|_| \_|  \___/  |___||_____| 
```

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20macOS%20%7C%20WSL-green.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Android-APK-red.svg" alt="Output">
  <img src="https://img.shields.io/badge/Languages-4-purple.svg" alt="Languages">
</p>

> **Transform websites into Android APKs without Android Studio hell.**
> 
> Build production-ready Android apps from any web project in minutes! 🚀

---

## ⚠️ IMPORTANT - READ FIRST!

### 📱 TERMUX USERS: You MUST use ZSH!

**Problem:** When you run `anvil` in Termux's default bash shell, you get:
```
anvil: command not found
```

**Solution:** You MUST open ZSH shell!

```bash
# AFTER installing ANVIL, run this command:
zsh

# Now you can use anvil
anvil --help
anvil init
```

**Why?** Termux uses bash by default, but ANVIL's launcher script is configured for zsh. Just type `zsh` and press Enter to switch.

---

## 📦 Installation Modes

ANVIL supports 4 installation modes to fit your needs:

| Mode | Size | Description | Use Case |
|------|------|-------------|----------|
| **light** | ~10MB | Minimal CLI only | Testing, quick builds |
| **normal** | ~50MB | Standard installation | Most users |
| **full** | ~2GB | Everything included | Full Android SDK |

### Quick Install (Normal Mode)
```bash
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash
```

### Light Mode (No SDK Required)
```bash
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash -s -- --mode light
```

### Full Mode (With Android SDK)
```bash
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash -s -- --mode full
```

---

## 🚀 Quick Start

### Step 1: Install
```bash
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash
```

### Step 2: Switch to ZSH (TERMUX ONLY)
```bash
zsh
```

### Step 3: Verify
```bash
anvil --version
anvil doctor
```

### Step 4: Create your first app
```bash
anvil init
```

### Step 5: Build APK
```bash
anvil build        # Full build (needs SDK)
anvil pack         # Light build (no SDK needed)
```

---

## 🔧 All Commands

| Command | Description | Example |
|---------|-------------|---------|
| `anvil init` | Create new project | `anvil init` |
| `anvil build` | Compile APK (needs SDK) | `anvil build` |
| `anvil build --release` | Build release APK | `anvil build --release` |
| `anvil build --low-memory` | Mobile build | `anvil build --low-memory` |
| `anvil pack` | Light build (no SDK) | `anvil pack` |
| `anvil quick-build` | Build from URL/GitHub/ZIP | `anvil quick-build --url https://github.com/user/repo` |
| `anvil sign` | Sign APK | `anvil sign --generate` |
| `anvil doctor` | Check system | `anvil doctor` |
| `anvil doctor --fix` | Auto-fix issues | `anvil doctor --fix` |
| `anvil preview` | Test in browser | `anvil preview` |
| `anvil deploy` | Install on device | `anvil deploy` |
| `anvil demo` | Create demo APK | `anvil demo` |
| `anvil lang` | Change language | `anvil lang --set pt` |
| `anvil lang --list` | List languages | `anvil lang --list` |
| `anvil lang --show` | Show current | `anvil lang --show` |
| `anvil update` | Update ANVIL | `anvil update` |
| `anvil update --check` | Check updates | `anvil update --check` |
| `anvil config` | Edit config | `anvil config --show` |
| `anvil setup` | Setup wizard | `anvil setup` |
| `anvil setup --install-sdk` | Install Android SDK | `anvil setup --install-sdk` |
| `anvil inspect <url>` | Analyze website | `anvil inspect https://example.com` |
| `anvil run` | Dev server with live reload | `anvil run` |
| `anvil clean` | Remove build artifacts | `anvil clean` |
| `anvil logs` | View build logs | `anvil logs` |
| `anvil plugin` | Manage plugins | `anvil plugin list` |

---

## 🌐 Changing Language

### Method 1: Interactive Menu
```bash
anvil lang
```

### Method 2: Direct Command
```bash
anvil lang --set pt   # Portuguese
anvil lang --set es   # Spanish
anvil lang --set zh   # Mandarin
anvil lang --set en   # English
```

### Supported Languages

| Code | Language | Flag |
|------|----------|------|
| `en` | English | 🇺🇸 |
| `pt` | Português | 🇧🇷 |
| `es` | Español | 🇪🇸 |
| `zh` | 中文 | 🇨🇳 |

---

## 📥 Installation Methods

### 📱 Termux (Android) - RECOMMENDED

#### Step 1: Update Termux
```bash
pkg update && pkg upgrade
```

#### Step 2: Install ANVIL (Choose your mode)
```bash
# Normal (~50MB)
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash

# Light (~10MB) - No SDK needed
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash -s -- --mode light

# Full (~2GB) - With Android SDK
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash -s -- --mode full
```

#### Step 3: **SWITCH TO ZSH** (CRITICAL!)
```bash
zsh
```

#### Step 4: Verify
```bash
anvil doctor
```

---

### 🐧 Linux

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip git openjdk-17-jdk

# Install ANVIL
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash

# Verify
anvil --version
```

---

### 🍎 macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install ANVIL
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash

# Verify
anvil --version
```

---

### 🪟 Windows (WSL)

```bash
# Install WSL if not installed
wsl --install

# In WSL terminal
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash

# Verify
anvil --version
```

---

## 🎓 Complete Tutorial

### For Termux Users

#### 1. First Time Setup
```bash
# Update and install dependencies
pkg update && pkg upgrade
pkg install python git openjdk-17

# Install ANVIL (light mode for mobile)
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash -s -- --mode light

# IMPORTANT: Switch to zsh
zsh

# Check system
anvil doctor

# Change language to Portuguese
anvil lang --set pt

# Create project
anvil init
```

#### 2. Creating a Project
```
When you run 'anvil init', you'll be asked:

1. Informações Básicas
   ├─ Nome do app: Meu App
   ├─ Nome do autor: João Silva
   ├─ Email: joao@email.com
   ├─ Website: https://meuapp.com (opcional)
   ├─ ID do pacote: com.exemplo.meuapp
   └─ Versão: 1.0.0

2. Fonte
   ├─ [1] Pasta local
   ├─ [2] URL do GitHub
   ├─ [3] Arquivo ZIP
   ├─ [4] Modelo inicial
   └─ [5] URL remota

3. Ícone
   └─ Caminho do ícone (PNG, min 512x512)

4. Tema
   ├─ [1] Claro
   ├─ [2] Escuro
   └─ [3] Padrão do sistema

5. Permissões
   └─ Selecione as permissões necessárias

6. Modo de Renderização
   ├─ [1] WebView (estável)
   └─ [2] APK Nativo (beta)
```

#### 3. Building the APK
```bash
# Inside your project folder
cd meu-projeto

# Light build (no SDK needed)
anvil pack -o meu-app.apk

# Or full build (needs SDK)
anvil build
```

---

## 🔨 Build Modes Explained

### `anvil pack` (Light Build)
- No Android SDK required
- Creates APK using minimal tools
- Works on mobile devices
- Good for quick testing

### `anvil build` (Full Build)
- Requires Android SDK
- Creates proper signed APKs
- Full optimization
- Ready for Play Store

### `anvil quick-build` (Quick Build)
- Build from GitHub, ZIP, or URL
- One command to APK
- Great for demos

---

## 📋 Project Configuration

Create `anvil.config.json` in your project folder:

```json
{
  "name": "My App",
  "author": "John Doe",
  "authorEmail": "john@example.com",
  "package": "com.example.myapp",
  "version": "1.0.0",
  "description": "My awesome app",
  "theme": "system",
  "renderMode": "webview",
  "permissions": ["internet", "camera"],
  "features": ["offline-cache", "biometric"]
}
```

---

## 🚀 Quick Build from URL

```bash
# From GitHub
anvil quick-build --url https://github.com/user/repo

# From ZIP
anvil quick-build --url https://example.com/app.zip

# With custom name
anvil quick-build --url https://github.com/user/repo --name "My App"
```

---

## 🔐 Signing APKs

### Generate Keystore
```bash
anvil sign --generate
```

### Sign Existing APK
```bash
anvil sign --keystore mykeystore.jks --alias myalias
```

---

## 📱 Termux-Specific Notes

### Why ZSH?
- Termux defaults to bash
- ANVIL's launcher is configured for zsh
- ZSH provides better shell experience

### How to Always Use ZSH in Termux:
1. Open Termux
2. Type `zsh` and press Enter
3. Now you can use `anvil` command

### Make ZSH Default:
```bash
# Edit ~/.bashrc to auto-start zsh
echo 'if [ -z "$ZSH_VERSION" ]; then exec zsh; fi' >> ~/.bashrc

# Restart Termux
```

### Exit ZSH:
```bash
# Type 'exit' to go back to bash
exit
```

---

## 🛠️ Requirements

### Termux (Mobile) - Light Mode
- Python 3.9+
- Git
- ~10MB storage

### Termux (Mobile) - Full Mode
- Python 3.9+
- Git
- OpenJDK 17
- ~2GB storage (for Android SDK)

### Desktop
- Python 3.9+
- Java JDK 11+
- Git

---

## 🔧 Troubleshooting

### Problem: "anvil: command not found"

**Cause:** You're in bash shell, not zsh (Termux)

**Solution:**
```bash
# Type zsh and press Enter
zsh

# Now try
anvil --version
```

---

### Problem: "No module named 'anvil_cli'"

**Solution:**
```bash
# Reinstall ANVIL
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash

# Switch to zsh
zsh

# Try again
anvil --version
```

---

### Problem: "Java not found"

**Solution (Termux):**
```bash
pkg install openjdk-17
```

**Solution (Linux):**
```bash
sudo apt install openjdk-17-jdk
```

---

### Problem: Still having issues?

**Full reset:**
```bash
# Remove ANVIL completely
rm -rf ~/.anvil

# Reinstall
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash

# Switch to zsh
zsh

# Test
anvil --version
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         ANVIL CLI                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │   init   │───▶│  build   │───▶│   sign   │            │
│  └──────────┘    └──────────┘    └──────────┘            │
│       │              │               │                     │
│       ▼              ▼               ▼                     │
│  ┌────────────────────────────────────────────────────┐   │
│  │              Project Generator                      │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐   │   │
│  │  │ Gradle │  │Assets  │  │Manifest│  │ Icons  │   │   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘   │   │
│  └────────────────────────────────────────────────────┘   │
│                              │                              │
│                              ▼                              │
│                    ┌─────────────────┐                    │
│                    │    APK File    │                    │
│                    └─────────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Contributions welcome!

---

## 📄 License

MIT License

---

<p align="center">
  <strong>Made with ❤️ for developers worldwide</strong>
  <br>
  <a href="https://github.com/whesley264-oss/anvil">GitHub</a> •
  <a href="https://github.com/whesley264-oss/anvil/issues">Issues</a>
</p>