"""
ANVIL Generator - Generate Android project structure
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(step: str, message: str):
    print(f"\n{Colors.BOLD}[{step}]{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def ensure_dir(path: Path):
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)

def generate_android_project(project_dir: Path, config: Dict[str, Any]):
    """Generate complete Android project structure"""
    
    android_dir = project_dir / "android"
    app_dir = android_dir / "app"
    src_dir = app_dir / "src" / "main"
    
    # Clean existing if present
    if android_dir.exists():
        print_info(f"Removing existing android directory...")
        shutil.rmtree(android_dir)
    
    # Determine language (for native mode)
    language = config.get("language", "kotlin")  # Default to Kotlin for native
    is_kotlin = language == "kotlin"
    
    # Create directory structure
    dirs = [
        android_dir / "gradle" / "wrapper",
        src_dir / "java" / config["package"].replace(".", "/"),
        src_dir / "res" / "values",
        src_dir / "res" / "values-night",
        src_dir / "res" / "layout",
        src_dir / "res" / "menu",
        src_dir / "res" / "drawable",
        src_dir / "res" / "drawable-v24",
        src_dir / "res" / "mipmap-hdpi",
        src_dir / "res" / "mipmap-mdpi",
        src_dir / "res" / "mipmap-xhdpi",
        src_dir / "res" / "mipmap-xxhdpi",
        src_dir / "res" / "mipmap-xxxhdpi",
        src_dir / "res" / "mipmap-anydpi-v26",
        src_dir / "assets",
    ]
    
    for d in dirs:
        ensure_dir(d)
    
    # Generate Gradle files
    generate_gradle_files(android_dir, config)
    
    # Generate AndroidManifest.xml
    generate_manifest(src_dir / "AndroidManifest.xml", config)
    
    # Generate MainActivity
    if config.get("renderMode") == "webview":
        generate_webview_activity(
            src_dir / "java" / config["package"].replace(".", "/") / "MainActivity.kt",
            config, is_kotlin
        )
    else:
        generate_native_activity(
            src_dir / "java" / config["package"].replace(".", "/") / "MainActivity.kt",
            config, is_kotlin
        )
    
    # Generate Application class
    generate_app_class(
        src_dir / "java" / config["package"].replace(".", "/") / "AnvilApp.kt",
        config, is_kotlin
    )
    
    # Generate resources
    generate_resources(src_dir / "res", config)
    
    # Generate themes
    generate_themes(src_dir / "res", config)
    
    # Copy web source to assets
    copy_web_source(src_dir / "assets", config)
    
    print_success("Project structure created!")

def generate_gradle_files(android_dir: Path, config: Dict[str, Any]):
    """Generate Gradle build files"""
    
    # Get values
    project_name = config["name"]
    
    # settings.gradle.kts
    settings_content = f"""pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "{project_name}"
include(":app")
"""
    
    with open(android_dir / "settings.gradle.kts", "w") as f:
        f.write(settings_content)
    
    # build.gradle.kts (root)
    root_build = """// Top-level build file
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
}

tasks.register("clean", Delete::class) {
    delete(rootProject.layout.buildDirectory)
}
"""
    
    with open(android_dir / "build.gradle.kts", "w") as f:
        f.write(root_build)
    
    # gradle.properties
    gradle_props = """# Project-wide Gradle settings
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
android.nonTransitiveRClass=true
kotlin.code.style=official
"""
    
    with open(android_dir / "gradle.properties", "w") as f:
        f.write(gradle_props)
    
    # app/build.gradle.kts
    dependencies = []
    
    if "webview" in config.get("renderMode", ""):
        dependencies.extend([
            'implementation("androidx.webkit:webkit:1.10.0")',
            'implementation("com.google.android.material:material:1.11.0")',
        ])
    else:
        dependencies.extend([
            'implementation("androidx.appcompat:appcompat:1.6.1")',
            'implementation("com.google.android.material:material:1.11.0")',
            'implementation("androidx.constraintlayout:constraintlayout:2.1.4")',
        ])
    
    if "offline-cache" in config.get("features", []):
        dependencies.append('implementation("com.squareup.okhttp3:okhttp:4.12.0")')
    
    if "biometric" in config.get("features", []):
        dependencies.append('implementation("androidx.biometric:biometric:1.1.0")')
    
    # Always include swiperefreshlayout as it's used by default
    dependencies.append('implementation("androidx.swiperefreshlayout:swiperefreshlayout:1.1.0")')
    
    dep_string = "\n    ".join(dependencies)
    
    app_build = f"""plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "{config['package']}"
    compileSdk = 34

    defaultConfig {{
        applicationId = "{config['package']}"
        minSdk = 21
        targetSdk = 34
        versionCode = 1
        versionName = "{config['version']}"
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }}
    }}
    
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}
    
    kotlinOptions {{
        jvmTarget = "17"
    }}
    
    buildFeatures {{
        viewBinding = true
    }}
}}

dependencies {{
    {dep_string}
}}
"""
    
    with open(android_dir / "app" / "build.gradle.kts", "w") as f:
        f.write(app_build)
    
    # proguard-rules.pro
    pkg = config['package']
    proguard = f"""# ANVIL Proguard Rules
# Add project specific ProGuard rules here.

# Keep native methods
-keepclasseswithmembernames class * {{
    native <methods>;
}}

# Keep WebView
-keep class android.webkit.** {{ *; }}
-keep class * extends android.webkit.WebViewClient {{ *; }}

# Keep ANVIL classes
-keep class {pkg}.** {{ *; }}
"""
    
    with open(android_dir / "app" / "proguard-rules.pro", "w") as f:
        f.write(proguard)
    
    # gradle-wrapper.properties
    wrapper_props = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
    
    with open(android_dir / "gradle" / "wrapper" / "gradle-wrapper.properties", "w") as f:
        f.write(wrapper_props)
    
    # gradlew shell script - auto-installs gradle if needed
    gradlew_script = """#!/bin/bash
# ANVIL Gradle Wrapper - Downloads and uses correct Gradle version

set -x
ANDROID_DIR="$(cd "$(dirname "$0")" && pwd)"
GRADLE_USER_HOME="${GRADLE_USER_HOME:-$HOME/.gradle}"
GRADLE_VERSION="8.2"

# Use gradle from gradle-user-home if available, otherwise download
GRADLE_HOME_DIR="$GRADLE_USER_HOME/gradle-$GRADLE_VERSION"
GRADLE_BIN="$GRADLE_HOME_DIR/bin/gradle"

if [ ! -f "$GRADLE_BIN" ]; then
    echo "Downloading Gradle $GRADLE_VERSION..."
    
    # Use a writable temp directory
    if [ -n "$TERMUX_APP" ] || [ -d "$PREFIX" ]; then
        TMP_DIR="$HOME/.anvil/tmp/gradle_$$"
    else
        TMP_DIR="${TMPDIR:-/tmp}/anvil_gradle_$$"
    fi
    
    mkdir -p "$TMP_DIR"
    
    curl -sL "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" -o "$TMP_DIR/gradle.zip"
    unzip -q "$TMP_DIR/gradle.zip" -d "$TMP_DIR"
    
    mkdir -p "$GRADLE_USER_HOME"
    mv "$TMP_DIR/gradle-$GRADLE_VERSION" "$GRADLE_HOME_DIR"
    rm -rf "$TMP_DIR"
    
    echo "Gradle installed to: $GRADLE_HOME_DIR"
fi

export PATH="$GRADLE_HOME_DIR/bin:$PATH"
export GRADLE_USER_HOME

# Run gradle
exec gradle assembleDebug --no-daemon "$@"
"""
    
    gradlew_path = android_dir / "gradlew"
    with open(gradlew_path, "w") as f:
        f.write(gradlew_script)
    os.chmod(str(gradlew_path), 0o755)

def generate_manifest(manifest_path: Path, config: Dict[str, Any]):
    """Generate AndroidManifest.xml"""
    
    permissions_map = {
        "camera": 'android:name="android.permission.CAMERA"',
        "storage": 'android:name="android.permission.READ_EXTERNAL_STORAGE"',
        "bluetooth": 'android:name="android.permission.BLUETOOTH"',
        "notifications": 'android:name="android.permission.POST_NOTIFICATIONS"',
        "contacts": 'android:name="android.permission.READ_CONTACTS"',
        "location": 'android:name="android.permission.ACCESS_FINE_LOCATION"',
        "microphone": 'android:name="android.permission.RECORD_AUDIO"',
        "internet": 'android:name="android.permission.INTERNET"',
    }
    
    permissions_xml = []
    for perm in config.get("permissions", []):
        if perm in permissions_map:
            permissions_xml.append(f'    <uses-permission {permissions_map[perm]} />')
    
    perm_section = "\n    ".join(permissions_xml) if permissions_xml else ""
    
    manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

{perm_section}
{get_manifest_features(config)}

    <application
        android:name=".AnvilApp"
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.Anvil"
        android:usesCleartextTraffic="true"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.Anvil">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            
            <!-- Deep links -->
            {get_deep_links_filter(config)}
        </activity>
        
    </application>

</manifest>
"""
    
    with open(manifest_path, "w") as f:
        f.write(manifest)

def get_manifest_features(config: Dict[str, Any]) -> str:
    """Get feature declarations for manifest"""
    features = []
    
    if "camera" in config.get("permissions", []):
        features.append('    <uses-feature android:name="android.hardware.camera" android:required="false" />')
    
    if "location" in config.get("permissions", []):
        features.append('    <uses-feature android:name="android.hardware.location.gps" android:required="false" />')
    
    return "\n".join(features)

def get_deep_links_filter(config: Dict[str, Any]) -> str:
    """Get deep links intent filter"""
    if "deep-links" not in config.get("features", []):
        return ""
    
    return """<!-- Deep links -->
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="https" android:host="YOUR_DOMAIN.com" />
            </intent-filter>"""

def generate_webview_activity(path: Path, config: Dict[str, Any], is_kotlin: bool):
    """Generate WebView-based MainActivity"""
    
    # Get webview mode config
    webview_mode = config.get("webview", {}).get("mode", "local")
    remote_url = config.get("webview", {}).get("url", "")
    pkg = config["package"]
    features = config.get("features", [])
    has_pull_refresh = "pull-to-refresh" in features
    
    if is_kotlin:
        pull_refresh_code = ""
        if has_pull_refresh:
            pull_refresh_code = """
        swipeRefresh.setOnRefreshListener {{
            webView.reload()
        }}

        webView.webViewClient = object : WebViewClient() {{
            override fun onPageFinished(view: WebView?, url: String?) {{
                super.onPageFinished(view, url)
                swipeRefresh.isRefreshing = false
            }}
        }}"""
        
        activity = f"""package {pkg}

import android.annotation.SuppressLint
import android.content.pm.ApplicationInfo
import android.graphics.Bitmap
import android.os.Bundle
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout

class MainActivity : AppCompatActivity() {{

    private lateinit var webView: WebView
    private lateinit var swipeRefresh: SwipeRefreshLayout

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize views
        swipeRefresh = findViewById(R.id.swipeRefresh)
        webView = findViewById(R.id.webView)

        // Configure WebView
        webView.webViewClient = WebViewClient()
        webView.webChromeClient = object : WebChromeClient() {{
            override fun onProgressChanged(view: WebView?, newProgress: Int) {{
                super.onProgressChanged(view, newProgress)
            }}
        }}

        val webSettings = webView.settings
        webSettings.javaScriptEnabled = true
        webSettings.domStorageEnabled = true
        webSettings.cacheMode = WebSettings.LOAD_DEFAULT
        webSettings.allowFileAccess = true
        webSettings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW{pull_refresh_code}

        // Load content based on mode
        val url = when ("{webview_mode}") {{
            "remote" -> "{remote_url}"
            "hybrid" -> "{remote_url}"
            else -> "file:///android_asset/index.html"
        }}

        webView.loadUrl(url)
    }}

    @Deprecated("Deprecated in Java")
    @Suppress("DEPRECATION")
    override fun onBackPressed() {{
        if (webView.canGoBack()) {{
            webView.goBack()
        }} else {{
            super.onBackPressed()
        }}
    }}

    override fun onDestroy() {{
        webView.destroy()
        super.onDestroy()
    }}
}}
"""
    else:
        pkg = config["package"]
        features = config.get("features", [])
        has_pull = "pull-to-refresh" in features
        
        pull_code = ""
        if has_pull:
            pull_code = """
        // Pull-to-refresh
        swipeRefresh.setOnRefreshListener(() -> {{
            webView.reload();
        }});
        
        webView.setWebViewClient(new WebViewClient() {{
            @Override
            public void onPageFinished(WebView view, String url) {{
                super.onPageFinished(view, url);
                swipeRefresh.setRefreshing(false);
            }}
        }});"""
        
        activity = f"""package {pkg};

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

public class MainActivity extends AppCompatActivity {{

    private WebView webView;
    private SwipeRefreshLayout swipeRefresh;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize views
        swipeRefresh = findViewById(R.id.swipeRefresh);
        webView = findViewById(R.id.webView);

        // Configure WebView
        webView.setWebViewClient(new WebViewClient());
        
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
        webSettings.setAllowFileAccess(true);
        webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);{pull_code}

        // Load content based on mode
        String url;
        switch ("{webview_mode}") {{
            case "remote":
            case "hybrid":
                url = "{remote_url}";
                break;
            default:
                url = "file:///android_asset/index.html";
        }}

        webView.loadUrl(url);
    }}

    @Deprecated
    @Override
    public void onBackPressed() {{
        if (webView.canGoBack()) {{
            webView.goBack();
        }} else {{
            super.onBackPressed();
        }}
    }}

    @Override
    protected void onDestroy() {{
        webView.destroy();
        super.onDestroy();
    }}
}}
"""

    # Write file
    if is_kotlin:
        with open(path.with_suffix('.kt'), 'w') as f:
            f.write(activity)
    else:
        with open(path.with_suffix('.java'), 'w') as f:
            f.write(activity)

def generate_native_activity(path: Path, config: Dict[str, Any], is_kotlin: bool):
    """Generate Native Android MainActivity (without WebView)"""
    
    if is_kotlin:
        activity = f"""package {config["package"]}

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {{

    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Native Android UI implementation
        // Note: This is a placeholder for HTML-to-Android conversion
        // Full implementation converts HTML/CSS to Android Views
        
        val title = findViewById<TextView>(R.id.title)
        title.text = "{config['name']}"
    }}
}}
"""
    else:
        activity = f"""package {config["package"]};

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Native Android UI implementation
        // Note: This is a placeholder for HTML-to-Android conversion
        // Full implementation converts HTML/CSS to Android Views
        
        TextView title = findViewById(R.id.title);
        title.setText("{config['name']}");
    }}
}}
"""

    if is_kotlin:
        with open(path.with_suffix('.kt'), 'w') as f:
            f.write(activity)
    else:
        with open(path.with_suffix('.java'), 'w') as f:
            f.write(activity)

def generate_app_class(path: Path, config: Dict[str, Any], is_kotlin: bool):
    """Generate Application class"""
    
    if is_kotlin:
        app = f"""package {config["package"]}

import android.app.Application

class AnvilApp : Application() {{

    override fun onCreate() {{
        super.onCreate()
        // Initialize ANVIL components
    }}
}}
"""
    else:
        app = f"""package {config["package"]};

import android.app.Application;

public class AnvilApp extends Application {{

    @Override
    public void onCreate() {{
        super.onCreate();
        // Initialize ANVIL components
    }}
}}
"""

    if is_kotlin:
        with open(path.with_suffix('.kt'), 'w') as f:
            f.write(app)
    else:
        with open(path.with_suffix('.java'), 'w') as f:
            f.write(app)

def generate_resources(res_dir: Path, config: Dict[str, Any]):
    """Generate resource files"""
    
    # strings.xml
    strings = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{config["name"]}</string>
</resources>
"""
    
    with open(res_dir / "values" / "strings.xml", "w") as f:
        f.write(strings)
    
    # colors.xml
    splash_color = config.get("splash", {}).get("color", "#000000")
    colors = f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="splash_background">{splash_color}</color>
    <color name="primary">#2196F3</color>
    <color name="primary_dark">#1976D2</color>
    <color name="accent">#03DAC5</color>
</resources>
"""
    
    with open(res_dir / "values" / "colors.xml", "w") as f:
        f.write(colors)
    
    # activity_main.xml (WebView layout)
    activity_xml = """<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

"""
    
    # Always include SwipeRefreshLayout as it's used by default
    activity_xml += """    <androidx.swiperefreshlayout.widget.SwipeRefreshLayout
        android:id="@+id/swipeRefresh"
        android:layout_width="match_parent"
        android:layout_height="match_parent">

"""
    
    if config.get("renderMode") == "webview":
        activity_xml += """        <WebView
            android:id="@+id/webView"
            android:layout_width="match_parent"
            android:layout_height="match_parent" />

"""
    else:
        activity_xml += """        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical"
            android:padding="16dp">

            <TextView
                android:id="@+id/title"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:textSize="24sp"
                android:textStyle="bold" />

            <TextView
                android:id="@+id/description"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="8dp" />

        </LinearLayout>

"""
    
    # Always include closing tag for SwipeRefreshLayout
    activity_xml += """    </androidx.swiperefreshlayout.widget.SwipeRefreshLayout>

"""
    
    activity_xml += """</FrameLayout>
"""
    
    with open(res_dir / "layout" / "activity_main.xml", "w") as f:
        f.write(activity_xml)
    
    # launcher icon placeholders (simple XML)
    ic_launcher = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/primary"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
"""
    
    with open(res_dir / "mipmap-anydpi-v26" / "ic_launcher.xml", "w") as f:
        f.write(ic_launcher)
    
    with open(res_dir / "mipmap-anydpi-v26" / "ic_launcher_round.xml", "w") as f:
        f.write(ic_launcher)
    
    # Simple foreground drawable
    foreground = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M54,30 L74,70 L34,70 Z"/>
</vector>
"""
    
    with open(res_dir / "drawable" / "ic_launcher_foreground.xml", "w") as f:
        f.write(foreground)

def generate_themes(res_dir: Path, config: Dict[str, Any]):
    """Generate theme files"""
    
    theme_name = config.get("theme", "system")
    
    # Light theme
    light_theme = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.Anvil" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryDark">@color/primary_dark</item>
        <item name="colorAccent">@color/accent</item>
        <item name="android:statusBarColor">@color/primary_dark</item>
        <item name="android:windowBackground">@android:color/white</item>
    </style>
</resources>
"""
    
    with open(res_dir / "values" / "themes.xml", "w") as f:
        f.write(light_theme)
    
    # Dark theme
    dark_theme = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.Anvil" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryDark">@color/primary_dark</item>
        <item name="colorAccent">@color/accent</item>
        <item name="android:statusBarColor">@color/primary_dark</item>
        <item name="android:windowBackground">@android:color/black</item>
    </style>
</resources>
"""
    
    with open(res_dir / "values-night" / "themes.xml", "w") as f:
        f.write(dark_theme)

def copy_web_source(assets_dir: Path, config: Dict[str, Any]):
    """Copy web source to assets folder"""
    
    source = config.get("source", "")
    project_dir = Path(config.get("project_dir", "."))
    
    if not source or source == ".":
        # Check if there's an index.html in the project root
        index_path = project_dir / "index.html"
        if index_path.exists():
            shutil.copy2(index_path, assets_dir / "index.html")
            
            # Copy other root-level files (not directories)
            for item in project_dir.iterdir():
                if item.is_file() and item.name not in ['anvil.config.json', 'README.md', '.DS_Store']:
                    dest = assets_dir / item.name
                    shutil.copy2(item, dest)
            
            print_success("Copied web files from project root")
            return
        
        # Create default index.html if none exists
        index_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + config["name"] + """</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container { text-align: center; }
        h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        p { opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>""" + config["name"] + """</h1>
        <p>Powered by ANVIL</p>
    </div>
</body>
</html>
"""
        
        with open(assets_dir / "index.html", "w") as f:
            f.write(index_html)
        
        print_info("Created default index.html")
        return
    
    # Handle different source types
    source_path = Path(source) if not source.startswith(('http://', 'https://')) else None
    
    if source_path and source_path.exists():
        # Copy all files from source to assets
        if source_path.is_dir():
            for item in source_path.rglob('*'):
                if item.is_file():
                    rel_path = item.relative_to(source_path)
                    dest = assets_dir / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest)
            print_success(f"Copied web files from {source}")
        else:
            shutil.copy2(source_path, assets_dir / source_path.name)
            print_success(f"Copied {source_path.name} to assets")

def build_apk(project_dir: Path, config: Dict[str, Any], sign: bool = False, low_memory: bool = False):
    """Build APK using Gradle"""
    
    # Ensure absolute path
    project_dir = project_dir.resolve()
    android_dir = project_dir / "android"
    
    # Auto-generate if missing
    if not android_dir.exists():
        print_info("Android project structure missing. Generating...")
        generate_android_project(project_dir, config)
    
    # Check if gradlew exists and use appropriate build method
    gradlew = android_dir / "gradlew"
    
    # Use gradlew script - it downloads and uses the correct gradle version
    if gradlew.exists():
        os.chmod(str(gradlew), 0o755)
        cmd = [str(gradlew), "assembleDebug"]
        print_info("Using gradlew script (auto-downloads correct Gradle version)")
    else:
        # Fallback to system gradle
        cmd = ["gradle", "assembleDebug"]
        print_info("Using system gradle")
    
    # Build environment - copy current environment and add Gradle settings
    build_env = os.environ.copy()
    build_env['GRADLE_USER_HOME'] = os.environ.get('GRADLE_USER_HOME', str(Path.home() / '.gradle'))
    build_env['JAVA_HOME'] = os.environ.get('JAVA_HOME', '')
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(android_dir.resolve()), # Use absolute path for cwd
            capture_output=True,
            text=True,
            timeout=600, # 10 minutes for mobile (slower)
            env=build_env
        )
        
        if result.returncode == 0:
            print_success("APK built successfully!")
            
            # Find APK
            apk_dir = android_dir / "app" / "build" / "outputs" / "apk" / "debug"
            if apk_dir.exists():
                apks = list(apk_dir.glob("*.apk"))
                if apks:
                    return apks[0]
        else:
            print(f"Build output:\n{result.stdout}")
            print(f"Build errors:\n{result.stderr}")
            
    except FileNotFoundError:
        print_warning("Gradle not found. Trying gradlew script...")
        
        if gradlew.exists():
            os.chmod(str(gradlew), 0o755)
            result = subprocess.run(
                [str(gradlew), "assembleDebug"],
                cwd=str(android_dir.resolve()),
                capture_output=True,
                text=True,
                timeout=600,
                env=build_env
            )
            if result.returncode == 0:
                apk_dir = android_dir / "app" / "build" / "outputs" / "apk" / "debug"
                if apk_dir.exists():
                    apks = list(apk_dir.glob("*.apk"))
                    if apks:
                        return apks[0]
            else:
                print(f"Build output:\n{result.stdout}")
                print(f"Build errors:\n{result.stderr}")
        else:
            print_warning("No gradle or gradlew found. Please install Gradle.")
    
    except subprocess.TimeoutExpired:
        print_warning("Build timed out. Check Gradle configuration.")
    
    return None