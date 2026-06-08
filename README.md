# 🔨 ANVIL - Transform Websites into Android APKs

```text
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


---

## [NEW] What's New (v0.4.0)

### New Commands

| Command | Description |
|---------|-------------|
| `anvil demo` | Create a demo APK to test your ANVIL installation |
| `anvil update` | Update ANVIL to the latest version |

### anvil demo

Just installed ANVIL? Test it immediately without creating a project!

```bash
anvil demo
```

This creates a beautiful welcome APK proving your installation works:

- [OK] "ANVIL is working!"
- [OK] "APK generated successfully"
- [OK] "Ready for production"
- [PHONE] Features showcase (WebView, Native APK, Fast Build, Secure)

Like `vue create` or `npm init` - test your setup instantly!

### anvil update

Keep ANVIL up-to-date with one command:

```bash
anvil update              # Check and update
anvil update --check      # Just check for updates
anvil update --force      # Force reinstall current version
```

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
```

### Step 4: Create your first app
```bash
anvil init
```

### Step 5: Build APK
```bash
anvil build
```

---

## 🌐 Changing Language

### Method 1: Interactive Menu
```bash
anvil lang
```
This shows a menu with all 4 languages. Select one and it's saved.

### Method 2: Direct Command
```bash
# Change to Portuguese
anvil lang --set pt

# Change to Spanish
anvil lang --set es

# Change to Mandarin
anvil lang --set zh

# Change to English
anvil lang --set en
```

### Method 3: Show Current Language
```bash
anvil lang --show
```

### List All Languages
```bash
anvil lang --list
```

**Note:** After changing language, the new language will apply to ALL ANVIL commands (init, build, doctor, etc.)

---

## 📥 Installation Methods

### 📱 Termux (Android) - RECOMMENDED

#### Step 1: Update Termux
```bash
pkg update && pkg upgrade
```

#### Step 2: Install dependencies
```bash
pkg install python git openjdk-17
```

#### Step 3: Install ANVIL
```bash
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash
```

#### Step 4: **SWITCH TO ZSH** (CRITICAL!)
```bash
zsh
```

#### Step 5: Verify
```bash
anvil --version
```

**If you get "command not found":**
```bash
# Check if launcher exists
ls -la $PREFIX/bin/anvil

# If not, recreate manually
cat > $PREFIX/bin/anvil << 'EOF'
#!/bin/bash
export ANVIL_HOME="$HOME/.anvil"
export PYTHONPATH="$ANVIL_HOME:$PYTHONPATH"
exec python3 "$ANVIL_HOME/anvil_cli.py" "$@"
EOF

chmod +x $PREFIX/bin/anvil

# Now try
zsh
anvil --version
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

# Install ANVIL
curl -s https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh | bash

# IMPORTANT: Switch to zsh
zsh

# Change language to Portuguese
anvil lang --set pt

# Check system
anvil doctor

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

# Compile
anvil build

# Result: dist/app-1.0.0.apk
```

#### 4. Installing on Device
```bash
# Connect device via USB with debugging enabled
anvil deploy

# Or use ADB directly
adb install dist/app-1.0.0.apk
```

---

## 📋 All Commands

| Command | Description | Example |
|---------|-------------|---------|
| `anvil init` | Create new project | `anvil init` |
| `anvil build` | Compile APK | `anvil build` |
| `anvil build --low-memory` | Mobile build | `anvil build --low-memory` |
| `anvil sign` | Generate keystore | `anvil sign --generate` |
| `anvil doctor` | Check system | `anvil doctor` |
| `anvil preview` | Test in browser | `anvil preview` |
| `anvil deploy` | Install device | `anvil deploy` |
| `anvil quick-build --url URL` | Fast build | `anvil quick-build --url https://github.com/user/repo` |
| `anvil lang` | Change language | `anvil lang --set pt` |
| `anvil lang --list` | List languages | `anvil lang --list` |
| `anvil lang --show` | Show current | `anvil lang --show` |
| `anvil demo` | Test installation | `anvil demo` |
| `anvil update` | Update ANVIL | `anvil update --check` |
| `anvil config` | Edit config | `anvil config --show` |
| `anvil plugin` | Manage plugins | `anvil plugin list` |
| `anvil setup` | Setup wizard | `anvil setup --termux` |

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

### Problem: Language not changing

**Solution:**
```bash
# Check current language
anvil lang --show

# Set language again
anvil lang --set pt

# Verify config file
cat ~/.anvil/config.json
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

## 🌐 Supported Languages

| Code | Language | Flag | Status |
|------|----------|------|--------|
| `en` | English | 🇺🇸 | Default |
| `pt` | Português | 🇧🇷 | ✅ |
| `es` | Español | 🇪🇸 | ✅ |
| `zh` | 中文 | 🇨🇳 | ✅ |

### Quick Language Reference:

| Task | Command |
|------|---------|
| Change to Portuguese | `anvil lang --set pt` |
| Change to Spanish | `anvil lang --set es` |
| Change to Mandarin | `anvil lang --set zh` |
| Change to English | `anvil lang --set en` |
| List all | `anvil lang --list` |
| Show current | `anvil lang --show` |

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

## 📦 Project Configuration

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

## 🛠️ Requirements

### Termux (Mobile)
- Python 3.9+
- Git
- OpenJDK 17
- Android SDK (optional for builds)

### Desktop
- Python 3.9+
- Java JDK 11+
- Android SDK
- Git

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
  <br>
  <br>
  ⭐ Star this repo if ANVIL helped you!
</p>