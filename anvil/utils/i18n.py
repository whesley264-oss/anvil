"""
ANVIL Localization System
Supports: English, Portuguese, Spanish, Mandarin

This module provides full internationalization for all ANVIL CLI commands.
Every string displayed to the user should go through this system.
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Optional

# Default language
DEFAULT_LANGUAGE = "en"

# Language configurations
LANGUAGES = {
    "en": {"name": "English", "native": "English", "code": "en", "flag": "🇺🇸"},
    "pt": {"name": "Portuguese", "native": "Português", "code": "pt", "flag": "🇧🇷"},
    "es": {"name": "Spanish", "native": "Español", "code": "es", "flag": "🇪🇸"},
    "zh": {"name": "Mandarin", "native": "中文", "code": "zh", "flag": "🇨🇳"},
}

# Complete translations dictionary
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # =====================
    # ENGLISH
    # =====================
    "en": {
        # CLI banner
        "banner_title": "ANVIL",
        "banner_tagline": "Transform websites into Android APKs",
        "banner_version": "Version",
        "banner_commands": "Available commands",
        
        # Commands
        "cmd_init": "Create new project from web app",
        "cmd_build": "Compile APK",
        "cmd_sign": "Generate keystore / sign APK",
        "cmd_doctor": "Check system requirements",
        "cmd_preview": "Test in browser/emulator",
        "cmd_config": "Manage anvil.config.json",
        "cmd_plugin": "Manage plugins",
        "cmd_deploy": "Build + install on device",
        "cmd_setup": "Setup ANVIL on different platforms",
        "cmd_quickbuild": "Quick build from URL",
        "cmd_lang": "Change language",
        
        # Init wizard
        "init_title": "Project Init Wizard",
        "init_step1": "Basic Information",
        "init_app_name": "App name",
        "init_author": "Author name",
        "init_email": "Author email",
        "init_website": "Website (optional)",
        "init_package": "Package ID",
        "init_package_hint": "Format: com.domain.app (must start with letter)",
        "init_version": "Version",
        "init_description": "Description",
        "init_step2": "Source",
        "init_source_type": "How to import source?",
        "init_local": "Local folder",
        "init_github": "GitHub URL",
        "init_zip": "ZIP file",
        "init_template": "Template starter",
        "init_remote": "Remote URL",
        "init_step3": "Icon",
        "init_icon": "Icon path (PNG, min 512x512)",
        "init_icon_optional": "Icon path (optional)",
        "init_step4": "Splash Screen",
        "init_splash_enable": "Enable splash screen?",
        "init_splash_color": "Background color (hex)",
        "init_splash_image": "Splash image (optional)",
        "init_step5": "Theme",
        "init_theme": "Theme",
        "init_theme_light": "Light",
        "init_theme_dark": "Dark",
        "init_theme_system": "System default (automatic)",
        "init_step6": "Permissions",
        "init_permissions": "Select required permissions",
        "init_step7": "Native Features",
        "init_features": "Enable features",
        "init_step8": "Render Mode",
        "init_render_mode": "Render mode",
        "init_render_webview": "WebView (stable)",
        "init_render_webview_desc": "APK wraps web app in Android WebView",
        "init_render_native": "Native APK (beta)",
        "init_render_native_desc": "Generates complete Android project",
        "init_language": "Language",
        "init_kotlin": "Kotlin (recommended) - Modern, concise, null-safe",
        "init_java": "Java - Classic, more examples online",
        "init_step9": "Publishing",
        "init_github_repo": "Create GitHub repository?",
        "init_private": "Private repository?",
        "init_step10": "WebView Mode",
        "init_webview_mode": "How to load content?",
        "init_local_assets": "Local assets (file:///android_asset/)",
        "init_remote_url": "Remote URL (https://app.example.com)",
        "init_hybrid": "Hybrid (cache + offline fallback) - recommended",
        
        # Questions/Inputs
        "input_enter": "Press ENTER to continue",
        "input_select": "Select",
        "input_cancel": "Cancel",
        "input_yes": "y",
        "input_no": "n",
        "input_default": "default",
        "input_choice": "Choice",
        
        # Status messages
        "status_step": "Step",
        "status_saved": "Config saved",
        "status_generated": "Android project generated",
        "status_built": "APK built successfully",
        "status_error": "Error occurred",
        "status_next_steps": "Next steps",
        "status_install_dependencies": "Install dependencies",
        "status_run_doctor": "Run 'anvil doctor' to check system",
        
        # Errors
        "error_invalid_package": "Invalid package ID format!",
        "error_package_format": "Format: com.domain.app (must start with letter)",
        "error_path_not_exist": "Path does not exist",
        "error_path_required": "Path cannot be empty",
        "error_choose_option": "Please enter a valid option",
        "error_enter_number": "Please enter a valid number",
        "error_config_not_found": "anvil.config.json not found!",
        "error_run_init_first": "Run 'anvil init' first to create a project.",
        
        # Doctor
        "doctor_title": "System Check",
        "doctor_checking": "Checking system requirements...",
        "doctor_java": "Java JDK",
        "doctor_gradle": "Gradle",
        "doctor_sdk": "Android SDK",
        "doctor_internet": "Internet",
        "doctor_keystore": "Keystore",
        "doctor_config": "Config",
        "doctor_installed": "Installed",
        "doctor_not_found": "Not found",
        "doctor_missing": "Missing",
        "doctor_fix": "Fix",
        "doctor_all_good": "All systems ready!",
        "doctor_found": "Found",
        "doctor_check_java": "Checking Java...",
        "doctor_check_gradle": "Checking Gradle...",
        "doctor_check_sdk": "Checking Android SDK...",
        
        # Build
        "build_title": "Build APK",
        "build_config": "App configuration",
        "build_starting": "Starting build...",
        "build_compiling": "Compiling Android project...",
        "build_success": "APK built successfully!",
        "build_failed": "Build failed!",
        "build_size": "Size",
        "build_copied": "Copied to",
        "build_console_output": "Console output",
        
        # Language command
        "lang_title": "Change Language",
        "lang_current": "Current language",
        "lang_select": "Select new language",
        "lang_changed": "Language changed to",
        "lang_restart": "Restart ANVIL to apply changes",
        "lang_available": "Available languages",
        
        # Sign
        "sign_title": "Sign APK",
        "sign_generate": "Generate keystore",
        "sign_keystore_path": "Keystore path",
        "sign_alias": "Alias",
        "sign_password": "Password",
        "sign_validity": "Validity (years)",
        "sign_created": "Keystore created successfully!",
        "sign_signed": "APK signed successfully!",
        "sign_enter_password": "Enter keystore password",
        "sign_enter_alias": "Enter alias name",
        "sign_confirm_password": "Confirm password",
        
        # Deploy
        "deploy_title": "Deploy",
        "deploy_device": "Device",
        "deploy_installing": "Installing APK...",
        "deploy_success": "App installed successfully!",
        "deploy_connecting": "Connecting to device...",
        "deploy_usb": "USB",
        "deploy_wifi": "WiFi",
        
        # Preview
        "preview_title": "Preview",
        "preview_starting": "Starting preview server...",
        "preview_url": "Preview URL",
        "preview_qr": "Scan QR code",
        "preview_stop": "Press Ctrl+C to stop",
        
        # Quick build
        "quickbuild_title": "Quick Build",
        "quickbuild_downloading": "Downloading source...",
        "quickbuild_processing": "Processing...",
        "quickbuild_building": "Building APK...",
        "quickbuild_success": "Build complete!",
        "quickbuild_url": "URL (GitHub, ZIP, or HTML)",
        "quickbuild_name": "App name",
        
        # Setup
        "setup_title": "Setup ANVIL",
        "setup_termux": "Termux setup wizard",
        "setup_sdk": "Android SDK installation",
        "setup_java": "Java installation",
        "setup_detected": "Detected platform",
        "setup_checking": "Checking dependencies...",
        "setup_installing": "Installing...",
        "setup_success": "Setup complete!",
        "setup_install_java": "Installing Java...",
        "setup_install_sdk": "Installing Android SDK...",
        "setup_need_java": "Java is required but not found",
        "setup_need_sdk": "Android SDK is required but not found",
        "setup_run_doctor": "Run 'anvil doctor' for detailed check",
        
        # Misc
        "confirm": "Confirm",
        "back": "Back",
        "skip": "Skip",
        "default": "default",
        "optional": "optional",
        "yes": "Yes",
        "no": "No",
        "done": "Done!",
        "continue": "Continue",
        
        # Help
        "help_examples": "Examples",
        "help_usage": "Usage",
        "help_options": "Options",
    },
    
    # =====================
    # PORTUGUESE (BRASIL)
    # =====================
    "pt": {
        # CLI banner
        "banner_title": "ANVIL",
        "banner_tagline": "Transforma sites em APKs Android",
        "banner_version": "Versão",
        "banner_commands": "Comandos disponíveis",
        
        # Commands
        "cmd_init": "Criar novo projeto a partir de web app",
        "cmd_build": "Compilar APK",
        "cmd_sign": "Gerar keystore / assinar APK",
        "cmd_doctor": "Verificar requisitos do sistema",
        "cmd_preview": "Testar no navegador/emulador",
        "cmd_config": "Gerenciar anvil.config.json",
        "cmd_plugin": "Gerenciar plugins",
        "cmd_deploy": "Compilar e instalar no dispositivo",
        "cmd_setup": "Configurar ANVIL em diferentes plataformas",
        "cmd_quickbuild": "Compilação rápida via URL",
        "cmd_lang": "Mudar idioma",
        
        # Init wizard
        "init_title": "Assistente de Criação de Projeto",
        "init_step1": "Informações Básicas",
        "init_app_name": "Nome do app",
        "init_author": "Nome do autor",
        "init_email": "Email do autor",
        "init_website": "Website (opcional)",
        "init_package": "ID do pacote",
        "init_package_hint": "Formato: com.dominio.app (deve começar com letra)",
        "init_version": "Versão",
        "init_description": "Descrição",
        "init_step2": "Fonte",
        "init_source_type": "Como importar a fonte?",
        "init_local": "Pasta local",
        "init_github": "URL do GitHub",
        "init_zip": "Arquivo ZIP",
        "init_template": "Modelo inicial",
        "init_remote": "URL remota",
        "init_step3": "Ícone",
        "init_icon": "Caminho do ícone (PNG, min 512x512)",
        "init_icon_optional": "Caminho do ícone (opcional)",
        "init_step4": "Tela de Abertura",
        "init_splash_enable": "Ativar tela de abertura?",
        "init_splash_color": "Cor de fundo (hex)",
        "init_splash_image": "Imagem de abertura (opcional)",
        "init_step5": "Tema",
        "init_theme": "Tema",
        "init_theme_light": "Claro",
        "init_theme_dark": "Escuro",
        "init_theme_system": "Padrão do sistema",
        "init_step6": "Permissões",
        "init_permissions": "Selecione as permissões necessárias",
        "init_step7": "Recursos Nativos",
        "init_features": "Habilitar recursos",
        "init_step8": "Modo de Renderização",
        "init_render_mode": "Modo de renderização",
        "init_render_webview": "WebView (estável)",
        "init_render_webview_desc": "APK envolve o web app no WebView do Android",
        "init_render_native": "APK Nativo (beta)",
        "init_render_native_desc": "Gera projeto Android completo",
        "init_language": "Linguagem",
        "init_kotlin": "Kotlin (recomendado) - Moderno, conciso, null-safe",
        "init_java": "Java - Clássico, mais exemplos online",
        "init_step9": "Publicação",
        "init_github_repo": "Criar repositório no GitHub?",
        "init_private": "Repositório privado?",
        "init_step10": "Modo WebView",
        "init_webview_mode": "Como carregar o conteúdo?",
        "init_local_assets": "Arquivos locais (file:///android_asset/)",
        "init_remote_url": "URL remota (https://app.exemplo.com)",
        "init_hybrid": "Híbrido (cache + fallback offline) - recomendado",
        
        # Questions/Inputs
        "input_enter": "Pressione ENTER para continuar",
        "input_select": "Selecione",
        "input_cancel": "Cancelar",
        "input_yes": "s",
        "input_no": "n",
        "input_default": "padrão",
        "input_choice": "Escolha",
        
        # Status messages
        "status_step": "Passo",
        "status_saved": "Configuração salva",
        "status_generated": "Projeto Android gerado",
        "status_built": "APK compilado com sucesso",
        "status_error": "Ocorreu um erro",
        "status_next_steps": "Próximos passos",
        "status_install_dependencies": "Instalar dependências",
        "status_run_doctor": "Execute 'anvil doctor' para verificar o sistema",
        
        # Errors
        "error_invalid_package": "Formato de ID de pacote inválido!",
        "error_package_format": "Formato: com.dominio.app (deve começar com letra)",
        "error_path_not_exist": "Caminho não existe",
        "error_path_required": "Caminho não pode estar vazio",
        "error_choose_option": "Por favor, escolha uma opção válida",
        "error_enter_number": "Por favor, digite um número válido",
        "error_config_not_found": "anvil.config.json não encontrado!",
        "error_run_init_first": "Execute 'anvil init' primeiro para criar um projeto.",
        
        # Doctor
        "doctor_title": "Verificação do Sistema",
        "doctor_checking": "Verificando requisitos do sistema...",
        "doctor_java": "Java JDK",
        "doctor_gradle": "Gradle",
        "doctor_sdk": "Android SDK",
        "doctor_internet": "Internet",
        "doctor_keystore": "Keystore",
        "doctor_config": "Configuração",
        "doctor_installed": "Instalado",
        "doctor_not_found": "Não encontrado",
        "doctor_missing": "Faltando",
        "doctor_fix": "Corrigir",
        "doctor_all_good": "Todos os sistemas prontos!",
        "doctor_found": "Encontrado",
        "doctor_check_java": "Verificando Java...",
        "doctor_check_gradle": "Verificando Gradle...",
        "doctor_check_sdk": "Verificando Android SDK...",
        
        # Build
        "build_title": "Compilar APK",
        "build_config": "Configuração do app",
        "build_starting": "Iniciando compilação...",
        "build_compiling": "Compilando projeto Android...",
        "build_success": "APK compilado com sucesso!",
        "build_failed": "Falha na compilação!",
        "build_size": "Tamanho",
        "build_copied": "Copiado para",
        "build_console_output": "Saída do console",
        
        # Language command
        "lang_title": "Mudar Idioma",
        "lang_current": "Idioma atual",
        "lang_select": "Selecione novo idioma",
        "lang_changed": "Idioma alterado para",
        "lang_restart": "Reinicie o ANVIL para aplicar as mudanças",
        "lang_available": "Idiomas disponíveis",
        
        # Sign
        "sign_title": "Assinar APK",
        "sign_generate": "Gerar keystore",
        "sign_keystore_path": "Caminho do keystore",
        "sign_alias": "Alias",
        "sign_password": "Senha",
        "sign_validity": "Validade (anos)",
        "sign_created": "Keystore criado com sucesso!",
        "sign_signed": "APK assinado com sucesso!",
        "sign_enter_password": "Digite a senha do keystore",
        "sign_enter_alias": "Digite o nome do alias",
        "sign_confirm_password": "Confirme a senha",
        
        # Deploy
        "deploy_title": "Instalar",
        "deploy_device": "Dispositivo",
        "deploy_installing": "Instalando APK...",
        "deploy_success": "App instalado com sucesso!",
        "deploy_connecting": "Conectando ao dispositivo...",
        "deploy_usb": "USB",
        "deploy_wifi": "WiFi",
        
        # Preview
        "preview_title": "Visualizar",
        "preview_starting": "Iniciando servidor de visualização...",
        "preview_url": "URL de visualização",
        "preview_qr": "Escaneie o QR code",
        "preview_stop": "Pressione Ctrl+C para parar",
        
        # Quick build
        "quickbuild_title": "Compilação Rápida",
        "quickbuild_downloading": "Baixando fonte...",
        "quickbuild_processing": "Processando...",
        "quickbuild_building": "Compilando APK...",
        "quickbuild_success": "Compilação completa!",
        "quickbuild_url": "URL (GitHub, ZIP ou HTML)",
        "quickbuild_name": "Nome do app",
        
        # Setup
        "setup_title": "Configurar ANVIL",
        "setup_termux": "Assistente de configuração do Termux",
        "setup_sdk": "Instalação do Android SDK",
        "setup_java": "Instalação do Java",
        "setup_detected": "Plataforma detectada",
        "setup_checking": "Verificando dependências...",
        "setup_installing": "Instalando...",
        "setup_success": "Configuração completa!",
        "setup_install_java": "Instalando Java...",
        "setup_install_sdk": "Instalando Android SDK...",
        "setup_need_java": "Java é necessário mas não foi encontrado",
        "setup_need_sdk": "Android SDK é necessário mas não foi encontrado",
        "setup_run_doctor": "Execute 'anvil doctor' para verificação detalhada",
        
        # Misc
        "confirm": "Confirmar",
        "back": "Voltar",
        "skip": "Pular",
        "default": "padrão",
        "optional": "opcional",
        "yes": "Sim",
        "no": "Não",
        "done": "Pronto!",
        "continue": "Continuar",
        
        # Help
        "help_examples": "Exemplos",
        "help_usage": "Uso",
        "help_options": "Opções",
    },
    
    # =====================
    # SPANISH
    # =====================
    "es": {
        # CLI banner
        "banner_title": "ANVIL",
        "banner_tagline": "Transforma sitios web en APKs Android",
        "banner_version": "Versión",
        "banner_commands": "Comandos disponibles",
        
        # Commands
        "cmd_init": "Crear nuevo proyecto desde web app",
        "cmd_build": "Compilar APK",
        "cmd_sign": "Generar keystore / firmar APK",
        "cmd_doctor": "Verificar requisitos del sistema",
        "cmd_preview": "Probar en navegador/emulador",
        "cmd_config": "Gestionar anvil.config.json",
        "cmd_plugin": "Gestionar plugins",
        "cmd_deploy": "Compilar e instalar en dispositivo",
        "cmd_setup": "Configurar ANVIL en diferentes plataformas",
        "cmd_quickbuild": "Compilación rápida desde URL",
        "cmd_lang": "Cambiar idioma",
        
        # Init wizard
        "init_title": "Asistente de Creación de Proyecto",
        "init_step1": "Información Básica",
        "init_app_name": "Nombre de la app",
        "init_author": "Nombre del autor",
        "init_email": "Email del autor",
        "init_website": "Sitio web (opcional)",
        "init_package": "ID del paquete",
        "init_package_hint": "Formato: com.dominio.app (debe empezar con letra)",
        "init_version": "Versión",
        "init_description": "Descripción",
        "init_step2": "Fuente",
        "init_source_type": "¿Cómo importar la fuente?",
        "init_local": "Carpeta local",
        "init_github": "URL de GitHub",
        "init_zip": "Archivo ZIP",
        "init_template": "Plantilla inicial",
        "init_remote": "URL remota",
        "init_step3": "Icono",
        "init_icon": "Ruta del icono (PNG, min 512x512)",
        "init_icon_optional": "Ruta del icono (opcional)",
        "init_step4": "Pantalla de Inicio",
        "init_splash_enable": "¿Habilitar pantalla de inicio?",
        "init_splash_color": "Color de fondo (hex)",
        "init_splash_image": "Imagen de inicio (opcional)",
        "init_step5": "Tema",
        "init_theme": "Tema",
        "init_theme_light": "Claro",
        "init_theme_dark": "Oscuro",
        "init_theme_system": "Predeterminado del sistema",
        "init_step6": "Permisos",
        "init_permissions": "Seleccione los permisos requeridos",
        "init_step7": "Características Nativas",
        "init_features": "Habilitar características",
        "init_step8": "Modo de Renderizado",
        "init_render_mode": "Modo de renderizado",
        "init_render_webview": "WebView (estable)",
        "init_render_webview_desc": "APK envuelve la web app en WebView de Android",
        "init_render_native": "APK Nativo (beta)",
        "init_render_native_desc": "Genera proyecto Android completo",
        "init_language": "Lenguaje",
        "init_kotlin": "Kotlin (recomendado) - Moderno, conciso, null-safe",
        "init_java": "Java - Clásico, más ejemplos en línea",
        "init_step9": "Publicación",
        "init_github_repo": "¿Crear repositorio en GitHub?",
        "init_private": "¿Repositorio privado?",
        "init_step10": "Modo WebView",
        "init_webview_mode": "¿Cómo cargar el contenido?",
        "init_local_assets": "Archivos locales (file:///android_asset/)",
        "init_remote_url": "URL remota (https://app.ejemplo.com)",
        "init_hybrid": "Híbrido (cache + fallback offline) - recomendado",
        
        # Questions/Inputs
        "input_enter": "Presione ENTER para continuar",
        "input_select": "Seleccione",
        "input_cancel": "Cancelar",
        "input_yes": "s",
        "input_no": "n",
        "input_default": "predeterminado",
        "input_choice": "Selección",
        
        # Status messages
        "status_step": "Paso",
        "status_saved": "Configuración guardada",
        "status_generated": "Proyecto Android generado",
        "status_built": "APK compilado exitosamente",
        "status_error": "Ocurrió un error",
        "status_next_steps": "Próximos pasos",
        "status_install_dependencies": "Instalar dependencias",
        "status_run_doctor": "Ejecute 'anvil doctor' para verificar el sistema",
        
        # Errors
        "error_invalid_package": "¡Formato de ID de paquete inválido!",
        "error_package_format": "Formato: com.dominio.app (debe empezar con letra)",
        "error_path_not_exist": "La ruta no existe",
        "error_path_required": "La ruta no puede estar vacía",
        "error_choose_option": "Por favor, seleccione una opción válida",
        "error_enter_number": "Por favor, ingrese un número válido",
        "error_config_not_found": "¡anvil.config.json no encontrado!",
        "error_run_init_first": "Ejecute 'anvil init' primero para crear un proyecto.",
        
        # Doctor
        "doctor_title": "Verificación del Sistema",
        "doctor_checking": "Verificando requisitos del sistema...",
        "doctor_java": "Java JDK",
        "doctor_gradle": "Gradle",
        "doctor_sdk": "Android SDK",
        "doctor_internet": "Internet",
        "doctor_keystore": "Keystore",
        "doctor_config": "Configuración",
        "doctor_installed": "Instalado",
        "doctor_not_found": "No encontrado",
        "doctor_missing": "Faltante",
        "doctor_fix": "Corregir",
        "doctor_all_good": "¡Todos los sistemas listos!",
        "doctor_found": "Encontrado",
        "doctor_check_java": "Verificando Java...",
        "doctor_check_gradle": "Verificando Gradle...",
        "doctor_check_sdk": "Verificando Android SDK...",
        
        # Build
        "build_title": "Compilar APK",
        "build_config": "Configuración de la app",
        "build_starting": "Iniciando compilación...",
        "build_compiling": "Compilando proyecto Android...",
        "build_success": "¡APK compilado exitosamente!",
        "build_failed": "¡Error en la compilación!",
        "build_size": "Tamaño",
        "build_copied": "Copiado a",
        "build_console_output": "Salida de consola",
        
        # Language command
        "lang_title": "Cambiar Idioma",
        "lang_current": "Idioma actual",
        "lang_select": "Seleccione nuevo idioma",
        "lang_changed": "Idioma cambiado a",
        "lang_restart": "Reinicie ANVIL para aplicar los cambios",
        "lang_available": "Idiomas disponibles",
        
        # Sign
        "sign_title": "Firmar APK",
        "sign_generate": "Generar keystore",
        "sign_keystore_path": "Ruta del keystore",
        "sign_alias": "Alias",
        "sign_password": "Contraseña",
        "sign_validity": "Validez (años)",
        "sign_created": "¡Keystore creado exitosamente!",
        "sign_signed": "¡APK firmado exitosamente!",
        "sign_enter_password": "Ingrese la contraseña del keystore",
        "sign_enter_alias": "Ingrese el nombre del alias",
        "sign_confirm_password": "Confirme la contraseña",
        
        # Deploy
        "deploy_title": "Instalar",
        "deploy_device": "Dispositivo",
        "deploy_installing": "Instalando APK...",
        "deploy_success": "¡App instalada exitosamente!",
        "deploy_connecting": "Conectando al dispositivo...",
        "deploy_usb": "USB",
        "deploy_wifi": "WiFi",
        
        # Preview
        "preview_title": "Vista Previa",
        "preview_starting": "Iniciando servidor de vista previa...",
        "preview_url": "URL de vista previa",
        "preview_qr": "Escanee el código QR",
        "preview_stop": "Presione Ctrl+C para detener",
        
        # Quick build
        "quickbuild_title": "Compilación Rápida",
        "quickbuild_downloading": "Descargando fuente...",
        "quickbuild_processing": "Procesando...",
        "quickbuild_building": "Compilando APK...",
        "quickbuild_success": "¡Compilación completa!",
        "quickbuild_url": "URL (GitHub, ZIP o HTML)",
        "quickbuild_name": "Nombre de la app",
        
        # Setup
        "setup_title": "Configurar ANVIL",
        "setup_termux": "Asistente de configuración de Termux",
        "setup_sdk": "Instalación de Android SDK",
        "setup_java": "Instalación de Java",
        "setup_detected": "Plataforma detectada",
        "setup_checking": "Verificando dependencias...",
        "setup_installing": "Instalando...",
        "setup_success": "¡Configuración completa!",
        "setup_install_java": "Instalando Java...",
        "setup_install_sdk": "Instalando Android SDK...",
        "setup_need_java": "Java es necesario pero no se encontró",
        "setup_need_sdk": "Android SDK es necesario pero no se encontró",
        "setup_run_doctor": "Ejecute 'anvil doctor' para verificación detallada",
        
        # Misc
        "confirm": "Confirmar",
        "back": "Volver",
        "skip": "Omitir",
        "default": "predeterminado",
        "optional": "opcional",
        "yes": "Sí",
        "no": "No",
        "done": "¡Hecho!",
        "continue": "Continuar",
        
        # Help
        "help_examples": "Ejemplos",
        "help_usage": "Uso",
        "help_options": "Opciones",
    },
    
    # =====================
    # MANDARIN (CHINESE)
    # =====================
    "zh": {
        # CLI banner
        "banner_title": "ANVIL",
        "banner_tagline": "将网站转换为Android APK",
        "banner_version": "版本",
        "banner_commands": "可用命令",
        
        # Commands
        "cmd_init": "从Web应用创建新项目",
        "cmd_build": "编译APK",
        "cmd_sign": "生成密钥库/签名APK",
        "cmd_doctor": "检查系统要求",
        "cmd_preview": "在浏览器/模拟器中测试",
        "cmd_config": "管理anvil.config.json",
        "cmd_plugin": "管理插件",
        "cmd_deploy": "编译并安装到设备",
        "cmd_setup": "在不同平台上设置ANVIL",
        "cmd_quickbuild": "从URL快速编译",
        "cmd_lang": "更改语言",
        
        # Init wizard
        "init_title": "项目创建向导",
        "init_step1": "基本信息",
        "init_app_name": "应用名称",
        "init_author": "作者姓名",
        "init_email": "作者邮箱",
        "init_website": "网站 (可选)",
        "init_package": "包ID",
        "init_package_hint": "格式: com.domain.app (必须以字母开头)",
        "init_version": "版本",
        "init_description": "描述",
        "init_step2": "来源",
        "init_source_type": "如何导入来源?",
        "init_local": "本地文件夹",
        "init_github": "GitHub URL",
        "init_zip": "ZIP文件",
        "init_template": "起始模板",
        "init_remote": "远程URL",
        "init_step3": "图标",
        "init_icon": "图标路径 (PNG, 最小 512x512)",
        "init_icon_optional": "图标路径 (可选)",
        "init_step4": "启动画面",
        "init_splash_enable": "启用启动画面?",
        "init_splash_color": "背景颜色 (十六进制)",
        "init_splash_image": "启动图片 (可选)",
        "init_step5": "主题",
        "init_theme": "主题",
        "init_theme_light": "浅色",
        "init_theme_dark": "深色",
        "init_theme_system": "跟随系统",
        "init_step6": "权限",
        "init_permissions": "选择所需的权限",
        "init_step7": "原生功能",
        "init_features": "启用功能",
        "init_step8": "渲染模式",
        "init_render_mode": "渲染模式",
        "init_render_webview": "WebView (稳定)",
        "init_render_webview_desc": "APK在Android WebView中包装Web应用",
        "init_render_native": "原生APK (测试版)",
        "init_render_native_desc": "生成完整的Android项目",
        "init_language": "语言",
        "init_kotlin": "Kotlin (推荐) - 现代、简洁、空安全",
        "init_java": "Java - 经典、更多在线示例",
        "init_step9": "发布",
        "init_github_repo": "创建GitHub仓库?",
        "init_private": "私有仓库?",
        "init_step10": "WebView模式",
        "init_webview_mode": "如何加载内容?",
        "init_local_assets": "本地文件 (file:///android_asset/)",
        "init_remote_url": "远程URL (https://app.example.com)",
        "init_hybrid": "混合模式 (缓存 + 离线回退) - 推荐",
        
        # Questions/Inputs
        "input_enter": "按Enter继续",
        "input_select": "选择",
        "input_cancel": "取消",
        "input_yes": "y",
        "input_no": "n",
        "input_default": "默认",
        "input_choice": "选择",
        
        # Status messages
        "status_step": "步骤",
        "status_saved": "配置已保存",
        "status_generated": "Android项目已生成",
        "status_built": "APK编译成功",
        "status_error": "发生错误",
        "status_next_steps": "下一步",
        "status_install_dependencies": "安装依赖项",
        "status_run_doctor": "运行 'anvil doctor' 检查系统",
        
        # Errors
        "error_invalid_package": "无效的包ID格式!",
        "error_package_format": "格式: com.domain.app (必须以字母开头)",
        "error_path_not_exist": "路径不存在",
        "error_path_required": "路径不能为空",
        "error_choose_option": "请输入有效的选项",
        "error_enter_number": "请输入有效的数字",
        "error_config_not_found": "未找到anvil.config.json!",
        "error_run_init_first": "运行 'anvil init' 首先创建项目。",
        
        # Doctor
        "doctor_title": "系统检查",
        "doctor_checking": "正在检查系统要求...",
        "doctor_java": "Java JDK",
        "doctor_gradle": "Gradle",
        "doctor_sdk": "Android SDK",
        "doctor_internet": "互联网",
        "doctor_keystore": "密钥库",
        "doctor_config": "配置",
        "doctor_installed": "已安装",
        "doctor_not_found": "未找到",
        "doctor_missing": "缺失",
        "doctor_fix": "修复",
        "doctor_all_good": "所有系统就绪!",
        "doctor_found": "已找到",
        "doctor_check_java": "正在检查Java...",
        "doctor_check_gradle": "正在检查Gradle...",
        "doctor_check_sdk": "正在检查Android SDK...",
        
        # Build
        "build_title": "编译APK",
        "build_config": "应用配置",
        "build_starting": "开始编译...",
        "build_compiling": "正在编译Android项目...",
        "build_success": "APK编译成功!",
        "build_failed": "编译失败!",
        "build_size": "大小",
        "build_copied": "已复制到",
        "build_console_output": "控制台输出",
        
        # Language command
        "lang_title": "更改语言",
        "lang_current": "当前语言",
        "lang_select": "选择新语言",
        "lang_changed": "语言已更改为",
        "lang_restart": "重启ANVIL以应用更改",
        "lang_available": "可用的语言",
        
        # Sign
        "sign_title": "签名APK",
        "sign_generate": "生成密钥库",
        "sign_keystore_path": "密钥库路径",
        "sign_alias": "别名",
        "sign_password": "密码",
        "sign_validity": "有效期 (年)",
        "sign_created": "密钥库创建成功!",
        "sign_signed": "APK签名成功!",
        "sign_enter_password": "输入密钥库密码",
        "sign_enter_alias": "输入别名",
        "sign_confirm_password": "确认密码",
        
        # Deploy
        "deploy_title": "安装",
        "deploy_device": "设备",
        "deploy_installing": "正在安装APK...",
        "deploy_success": "应用安装成功!",
        "deploy_connecting": "正在连接到设备...",
        "deploy_usb": "USB",
        "deploy_wifi": "WiFi",
        
        # Preview
        "preview_title": "预览",
        "preview_starting": "正在启动预览服务器...",
        "preview_url": "预览URL",
        "preview_qr": "扫描二维码",
        "preview_stop": "按Ctrl+C停止",
        
        # Quick build
        "quickbuild_title": "快速编译",
        "quickbuild_downloading": "正在下载来源...",
        "quickbuild_processing": "正在处理...",
        "quickbuild_building": "正在编译APK...",
        "quickbuild_success": "编译完成!",
        "quickbuild_url": "URL (GitHub、ZIP或HTML)",
        "quickbuild_name": "应用名称",
        
        # Setup
        "setup_title": "设置ANVIL",
        "setup_termux": "Termux设置向导",
        "setup_sdk": "Android SDK安装",
        "setup_java": "Java安装",
        "setup_detected": "检测到的平台",
        "setup_checking": "正在检查依赖项...",
        "setup_installing": "正在安装...",
        "setup_success": "设置完成!",
        "setup_install_java": "正在安装Java...",
        "setup_install_sdk": "正在安装Android SDK...",
        "setup_need_java": "需要Java但未找到",
        "setup_need_sdk": "需要Android SDK但未找到",
        "setup_run_doctor": "运行 'anvil doctor' 进行详细检查",
        
        # Misc
        "confirm": "确认",
        "back": "返回",
        "skip": "跳过",
        "default": "默认",
        "optional": "可选",
        "yes": "是",
        "no": "否",
        "done": "完成!",
        "continue": "继续",
        
        # Help
        "help_examples": "示例",
        "help_usage": "用法",
        "help_options": "选项",
    },
}


class i18n:
    """Internationalization handler - singleton pattern"""
    
    _instance = None
    _current_language = DEFAULT_LANGUAGE
    _loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(i18n, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_language(cls) -> str:
        """Get current language code"""
        if not cls._loaded:
            cls.load_language()
        return cls._current_language
    
    @classmethod
    def set_language(cls, lang_code: str) -> bool:
        """Set current language"""
        if lang_code not in LANGUAGES:
            return False
        
        cls._current_language = lang_code
        cls._loaded = True
        
        # Save to config
        cls._save_language(lang_code)
        
        return True
    
    @classmethod
    def t(cls, key: str, default: str = None) -> str:
        """Translate a key - main method for getting translations"""
        if not cls._loaded:
            cls.load_language()
        
        # Get translation for current language
        lang_dict = TRANSLATIONS.get(cls._current_language, TRANSLATIONS["en"])
        result = lang_dict.get(key, None)
        
        # Fallback to English if key not found
        if result is None:
            result = TRANSLATIONS["en"].get(key, default or key)
        
        return result
    
    @classmethod
    def load_language(cls):
        """Load language from config file"""
        config_file = Path.home() / ".anvil" / "config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                lang = config.get('language', DEFAULT_LANGUAGE)
                if lang in LANGUAGES:
                    cls._current_language = lang
            except:
                pass
        
        cls._loaded = True
    
    @classmethod
    def _save_language(cls, lang_code: str):
        """Save language to config"""
        config_file = Path.home() / ".anvil" / "config.json"
        config_dir = config_file.parent
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config = {}
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except:
                pass
        
        config['language'] = lang_code
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def get_available_languages(cls) -> Dict:
        """Get all available languages"""
        return LANGUAGES
    
    @classmethod
    def get_translations(cls, lang_code: str = None) -> Dict:
        """Get all translations for a language"""
        if lang_code is None:
            lang_code = cls._current_language
        return TRANSLATIONS.get(lang_code, TRANSLATIONS["en"])


# Global function for easy access
def _(key: str, default: str = None) -> str:
    """Translate a key using global i18n instance"""
    return i18n.t(key, default)


def get_translator():
    """Get a translator function for the current language"""
    return lambda key, default=None: i18n.t(key, default)


# Initialize on module load
i18n.load_language()