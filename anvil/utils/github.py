"""
ANVIL GitHub utilities
Interactive configuration - asks for username and token when needed
"""

import os
import urllib.request
import json

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def configure_github():
    """Interactive GitHub configuration - ask for username and token"""
    
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════╗")
    print("║        GitHub Configuration              ║")
    print("╚══════════════════════════════════════════╝{Colors.END}\n")
    
    print_info("To create GitHub repositories, you need to configure your credentials.\n")
    
    username = input(f"{Colors.BOLD}GitHub Username{Colors.END}: ").strip()
    
    if not username:
        print_error("Username is required")
        return None, None
    
    print_info("Create a Personal Access Token at: https://github.com/settings/tokens/new")
    print_info("Scopes needed: 'repo' (full control of repositories)\n")
    
    token = input(f"{Colors.BOLD}GitHub Token{Colors.END}: ").strip()
    
    if not token:
        print_error("Token is required")
        return None, None
    
    # Validate by testing the token
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        req = urllib.request.Request('https://api.github.com/user', headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            confirmed_username = data.get('login', username)
            
            if confirmed_username.lower() != username.lower():
                print_warning(f"Token belongs to '{confirmed_username}', not '{username}'")
                response = input("Continue anyway? [y/N]: ").strip().lower()
                if response not in ['y', 'yes']:
                    return None, None
            
            print_success(f"Authenticated as: {confirmed_username}")
            
            # Save config
            save_github_config(username, token)
            
            return username, token
            
    except Exception as e:
        print_error(f"Invalid token: {e}")
        return None, None

def save_github_config(username: str, token: str):
    """Save GitHub configuration to file"""
    from pathlib import Path
    
    config_dir = Path.home() / ".anvil"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.json"
    
    config = {}
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except:
            pass
    
    config['github_token'] = token
    config['github_username'] = username
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print_success(f"Config saved to: {config_file}")

def load_github_config():
    """Load GitHub configuration from file"""
    from pathlib import Path
    
    config_file = Path.home() / ".anvil" / "config.json"
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            token = config.get('github_token', '')
            username = config.get('github_username', '')
            
            if token and username:
                os.environ['GITHUB_TOKEN'] = token
                return username, token
        except:
            pass
    
    return None, None

def get_github_credentials():
    """Get GitHub credentials, asking if not configured"""
    username, token = load_github_config()
    
    if token and username:
        return username, token
    
    # Ask to configure
    print_info("GitHub credentials not found.")
    response = input("Configure GitHub now? [y/N]: ").strip().lower()
    
    if response in ['y', 'yes']:
        return configure_github()
    
    return None, None

def github_api_request(method: str, endpoint: str, data: dict = None, token: str = None) -> tuple:
    """Make a GitHub API request"""
    
    if not token:
        _, token = load_github_config()
    
    if not token:
        return 401, {"error": "GitHub token not configured"}
    
    url = f"https://api.github.com{endpoint}"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, method=method, headers=headers)
        
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return response.status, result
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get('message', str(e))
        except:
            error_msg = str(e)
        return e.code, {"error": error_msg}
    except Exception as e:
        return 500, {"error": str(e)}

def get_username(token: str = None) -> str:
    """Get authenticated GitHub username"""
    status, data = github_api_request("GET", "/user", token=token)
    
    if status == 200:
        return data.get('login', '')
    
    return ''

def create_github_repo(name: str, description: str = "", private: bool = True, auto_init: bool = True) -> str:
    """Create a GitHub repository"""
    
    username, token = get_github_credentials()
    
    if not username or not token:
        print_warning("GitHub not configured. Run 'anvil init' and configure when prompted.")
        return None
    
    # Prepare repository data
    repo_data = {
        "name": name.lower().replace(' ', '-').replace('_', '-'),
        "description": description or f"ANVIL project: {name}",
        "private": private,
        "auto_init": auto_init,
        "has_issues": True,
        "has_wiki": False,
        "has_downloads": False
    }
    
    print_info(f"Creating repository: {repo_data['name']}")
    
    status, response = github_api_request("POST", "/user/repos", repo_data, token=token)
    
    if status == 201:
        repo_url = f"https://github.com/{username}/{repo_data['name']}"
        print_success(f"Repository created: {repo_url}")
        return repo_url
    else:
        error_msg = response.get('error', 'Unknown error')
        
        if 'already exists' in error_msg.lower():
            repo_url = f"https://github.com/{username}/{repo_data['name']}"
            print_warning(f"Repository already exists: {repo_url}")
            return repo_url
        
        print_error(f"Failed to create repository: {error_msg}")
        return None

def push_to_github(repo_name: str, files: dict, commit_message: str = "Update via ANVIL") -> bool:
    """Push files to GitHub repository"""
    
    username, token = get_github_credentials()
    
    if not username or not token:
        return False
    
    # Get current commit SHA
    status, ref_data = github_api_request("GET", f"/repos/{username}/{repo_name}/git/ref/heads/main", token=token)
    
    if status != 200:
        status, ref_data = github_api_request("GET", f"/repos/{username}/{repo_name}/git/ref/heads/master", token=token)
    
    if status != 200:
        print_error(f"Repository not found: {repo_name}")
        return False
    
    current_sha = ref_data.get('object', {}).get('sha')
    
    # Get tree SHA
    status, commit_data = github_api_request("GET", f"/repos/{username}/{repo_name}/git/commits/{current_sha}", token=token)
    
    if status != 200:
        print_error("Could not get commit data")
        return False
    
    tree_sha = commit_data.get('tree', {}).get('sha')
    
    # Create tree with files
    tree_items = []
    for path, content in files.items():
        tree_items.append({
            "path": path,
            "mode": "100644",
            "type": "blob",
            "content": content
        })
    
    # Create new tree
    status, tree_data = github_api_request("POST", f"/repos/{username}/{repo_name}/git/trees", {
        "base_tree": tree_sha,
        "tree": tree_items
    }, token=token)
    
    if status != 201:
        print_error(f"Failed to create tree: {tree_data.get('error', 'Unknown')}")
        return False
    
    tree_sha = tree_data.get('sha')
    
    # Create commit
    status, commit_data = github_api_request("POST", f"/repos/{username}/{repo_name}/git/commits", {
        "message": commit_message,
        "tree": tree_sha,
        "parents": [current_sha]
    }, token=token)
    
    if status != 201:
        print_error(f"Failed to create commit: {commit_data.get('error', 'Unknown')}")
        return False
    
    commit_sha = commit_data.get('sha')
    
    # Update reference
    branch = "main"
    status, _ = github_api_request("PATCH", f"/repos/{username}/{repo_name}/git/refs/heads/{branch}", {
        "sha": commit_sha,
        "force": False
    }, token=token)
    
    if status == 200:
        print_success(f"Files pushed to {username}/{repo_name}")
        return True
    else:
        print_error("Failed to update branch")
        return False

def create_pull_request(repo: str, title: str, body: str, head: str, base: str = "main") -> dict:
    """Create a pull request"""
    
    username, token = get_github_credentials()
    
    if not username or not token:
        return {"error": "Not configured"}
    
    if ':' not in head:
        head = f"{username}:{head}"
    
    pr_data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }
    
    status, response = github_api_request("POST", f"/repos/{username}/{repo}/pulls", pr_data, token=token)
    
    if status == 201:
        return response
    else:
        return {"error": response.get('error', 'Unknown error')}

def get_repos() -> list:
    """Get list of user repositories"""
    
    username, token = get_github_credentials()
    
    if not username or not token:
        return []
    
    status, data = github_api_request("GET", "/user/repos?per_page=100&sort=updated", token=token)
    
    if status == 200:
        return data
    return []

# Load config on module import
load_github_config()