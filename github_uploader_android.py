#!/usr/bin/env python3
"""
GITHUB UPLOADER FOR ANDROID
Automates GitHub uploads from Android tablet using Pydroid

Features:
- Push files to GitHub repository
- Commit changes with custom messages
- Browse and select files to upload
- Create new files directly
- View repository status
- Works without root on Android

Requires:
- requests library: pip install requests
- Personal Access Token from GitHub

By Adam Lee Hatchett
"""

import os
import json
import base64
import hashlib
import threading
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    requests = None

try:
    import tkinter as tk
    from tkinter import scrolledtext, messagebox, filedialog, simpledialog
except ImportError:
    print("tkinter not available - CLI mode only")
    tk = None


class GitHubAPI:
    """GitHub API wrapper for repository operations."""

    def __init__(self, token=None, owner=None, repo=None):
        """
        Initialize GitHub API client.

        Args:
            token: GitHub Personal Access Token
            owner: Repository owner (username or organization)
            repo: Repository name
        """
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.config_file = "github_uploader_config.json"
        self._load_config()

    def _load_config(self):
        """Load saved configuration."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if not self.token:
                        self.token = config.get('token')
                    if not self.owner:
                        self.owner = config.get('owner')
                    if not self.repo:
                        self.repo = config.get('repo')
            except (json.JSONDecodeError, IOError):
                pass

    def save_config(self):
        """Save configuration (excluding token for security)."""
        config = {
            'owner': self.owner,
            'repo': self.repo
            # Note: Token is NOT saved for security reasons
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config: {e}")

    def _headers(self):
        """Get request headers with authentication."""
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Uploader-Android'
        }
        if self.token:
            headers['Authorization'] = f'token {self.token}'
        return headers

    def _make_request(self, method, endpoint, **kwargs):
        """Make an API request with error handling."""
        if not requests:
            return {'error': 'requests library not installed'}

        url = f"{self.base_url}{endpoint}"
        kwargs['headers'] = self._headers()

        try:
            response = requests.request(method, url, timeout=30, **kwargs)
            if response.status_code in (200, 201):
                return response.json() if response.content else {}
            elif response.status_code == 404:
                return {'error': 'Not found - check repository name and permissions'}
            elif response.status_code == 401:
                return {'error': 'Authentication failed - check your token'}
            elif response.status_code == 422:
                error_data = response.json()
                return {'error': f"Validation failed: {error_data.get('message', 'Unknown error')}"}
            else:
                return {'error': f"HTTP {response.status_code}: {response.text[:200]}"}
        except requests.exceptions.Timeout:
            return {'error': 'Request timed out - check your internet connection'}
        except requests.exceptions.ConnectionError:
            return {'error': 'Connection failed - check your internet connection'}
        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {str(e)}'}

    def test_connection(self):
        """Test API connection and authentication."""
        result = self._make_request('GET', '/user')
        if 'error' in result:
            return False, result['error']
        return True, f"Connected as: {result.get('login', 'Unknown')}"

    def get_repo_info(self):
        """Get repository information."""
        if not self.owner or not self.repo:
            return {'error': 'Repository not configured'}
        return self._make_request('GET', f'/repos/{self.owner}/{self.repo}')

    def list_contents(self, path=''):
        """List contents of a directory in the repository."""
        if not self.owner or not self.repo:
            return {'error': 'Repository not configured'}
        endpoint = f'/repos/{self.owner}/{self.repo}/contents/{path}'
        return self._make_request('GET', endpoint)

    def get_file(self, path):
        """Get a file's content and metadata."""
        if not self.owner or not self.repo:
            return {'error': 'Repository not configured'}
        endpoint = f'/repos/{self.owner}/{self.repo}/contents/{path}'
        return self._make_request('GET', endpoint)

    def create_or_update_file(self, path, content, message, branch='main'):
        """
        Create or update a file in the repository.

        Args:
            path: File path in the repository
            content: File content (string or bytes)
            message: Commit message
            branch: Branch name (default: main)

        Returns:
            dict with result or error
        """
        if not self.owner or not self.repo:
            return {'error': 'Repository not configured'}

        # Encode content to base64
        if isinstance(content, str):
            content_bytes = content.encode('utf-8')
        else:
            content_bytes = content
        content_b64 = base64.b64encode(content_bytes).decode('utf-8')

        # Check if file exists to get SHA (required for updates)
        existing = self.get_file(path)
        sha = existing.get('sha') if 'error' not in existing else None

        # Prepare request data
        data = {
            'message': message,
            'content': content_b64,
            'branch': branch
        }
        if sha:
            data['sha'] = sha

        endpoint = f'/repos/{self.owner}/{self.repo}/contents/{path}'
        return self._make_request('PUT', endpoint, json=data)

    def delete_file(self, path, message, branch='main'):
        """Delete a file from the repository."""
        if not self.owner or not self.repo:
            return {'error': 'Repository not configured'}

        # Get file SHA (required for deletion)
        existing = self.get_file(path)
        if 'error' in existing:
            return existing

        sha = existing.get('sha')
        if not sha:
            return {'error': 'Could not get file SHA'}

        data = {
            'message': message,
            'sha': sha,
            'branch': branch
        }

        endpoint = f'/repos/{self.owner}/{self.repo}/contents/{path}'
        return self._make_request('DELETE', endpoint, json=data)

    def upload_local_file(self, local_path, repo_path=None, message=None, branch='main'):
        """
        Upload a local file to the repository.

        Args:
            local_path: Path to local file
            repo_path: Path in repository (default: same as filename)
            message: Commit message (default: "Upload {filename}")
            branch: Branch name

        Returns:
            dict with result or error
        """
        local_path = Path(local_path)
        if not local_path.exists():
            return {'error': f'File not found: {local_path}'}

        if repo_path is None:
            repo_path = local_path.name

        if message is None:
            message = f"Upload {local_path.name}"

        try:
            with open(local_path, 'rb') as f:
                content = f.read()
        except IOError as e:
            return {'error': f'Could not read file: {e}'}

        return self.create_or_update_file(repo_path, content, message, branch)

    def get_branches(self):
        """List repository branches."""
        if not self.owner or not self.repo:
            return {'error': 'Repository not configured'}
        return self._make_request('GET', f'/repos/{self.owner}/{self.repo}/branches')

    def get_commits(self, branch='main', per_page=10):
        """Get recent commits."""
        if not self.owner or not self.repo:
            return {'error': 'Repository not configured'}
        endpoint = f'/repos/{self.owner}/{self.repo}/commits'
        params = {'sha': branch, 'per_page': per_page}
        return self._make_request('GET', endpoint, params=params)


class GitHubUploaderGUI:
    """Android-friendly GUI for GitHub uploads."""

    def __init__(self):
        self.api = GitHubAPI()

        self.root = tk.Tk()
        self.root.title("GitHub Uploader - Android")
        self.root.geometry("800x700")

        self._create_ui()

        # Check configuration on startup
        self.root.after(500, self._check_config)

    def _create_ui(self):
        """Create the user interface."""
        # Header
        header = tk.Frame(self.root, bg='#24292e', height=60)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="📤 GITHUB UPLOADER",
            font=("Arial", 20, "bold"),
            bg='#24292e',
            fg='white'
        ).pack(pady=15)

        # Configuration panel
        config_frame = tk.LabelFrame(
            self.root,
            text="⚙️ Configuration",
            font=("Arial", 12, "bold")
        )
        config_frame.pack(fill=tk.X, padx=10, pady=5)

        # Token entry
        token_frame = tk.Frame(config_frame)
        token_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            token_frame,
            text="Token:",
            font=("Arial", 11),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.token_entry = tk.Entry(token_frame, font=("Courier", 10), show="*")
        self.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            token_frame,
            text="👁",
            command=self._toggle_token_visibility,
            font=("Arial", 10)
        ).pack(side=tk.LEFT)

        # Owner entry
        owner_frame = tk.Frame(config_frame)
        owner_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            owner_frame,
            text="Owner:",
            font=("Arial", 11),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.owner_entry = tk.Entry(owner_frame, font=("Courier", 10))
        self.owner_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Repo entry
        repo_frame = tk.Frame(config_frame)
        repo_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            repo_frame,
            text="Repository:",
            font=("Arial", 11),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.repo_entry = tk.Entry(repo_frame, font=("Courier", 10))
        self.repo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Branch entry
        branch_frame = tk.Frame(config_frame)
        branch_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            branch_frame,
            text="Branch:",
            font=("Arial", 11),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.branch_entry = tk.Entry(branch_frame, font=("Courier", 10))
        self.branch_entry.insert(0, "main")
        self.branch_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Config buttons
        config_btn_frame = tk.Frame(config_frame)
        config_btn_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(
            config_btn_frame,
            text="🔗 Test Connection",
            command=self._test_connection,
            bg='#2ea44f',
            fg='white',
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)

        tk.Button(
            config_btn_frame,
            text="💾 Save Config",
            command=self._save_config,
            bg='#0366d6',
            fg='white',
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)

        # Upload panel
        upload_frame = tk.LabelFrame(
            self.root,
            text="📁 Upload Files",
            font=("Arial", 12, "bold")
        )
        upload_frame.pack(fill=tk.X, padx=10, pady=5)

        # File selection
        file_frame = tk.Frame(upload_frame)
        file_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            file_frame,
            text="File:",
            font=("Arial", 11),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.file_entry = tk.Entry(file_frame, font=("Courier", 10))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            file_frame,
            text="📂 Browse",
            command=self._browse_file,
            font=("Arial", 10)
        ).pack(side=tk.LEFT)

        # Remote path
        remote_frame = tk.Frame(upload_frame)
        remote_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            remote_frame,
            text="Remote Path:",
            font=("Arial", 11),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.remote_entry = tk.Entry(remote_frame, font=("Courier", 10))
        self.remote_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Commit message
        msg_frame = tk.Frame(upload_frame)
        msg_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            msg_frame,
            text="Message:",
            font=("Arial", 11),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.message_entry = tk.Entry(msg_frame, font=("Courier", 10))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Upload buttons
        upload_btn_frame = tk.Frame(upload_frame)
        upload_btn_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(
            upload_btn_frame,
            text="📤 Upload File",
            command=self._upload_file,
            bg='#2ea44f',
            fg='white',
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)

        tk.Button(
            upload_btn_frame,
            text="✏️ Create New File",
            command=self._create_new_file,
            bg='#6f42c1',
            fg='white',
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)

        # Repository browser
        browser_frame = tk.LabelFrame(
            self.root,
            text="📋 Repository Contents",
            font=("Arial", 12, "bold")
        )
        browser_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        browser_btn_frame = tk.Frame(browser_frame)
        browser_btn_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Button(
            browser_btn_frame,
            text="🔄 Refresh",
            command=self._refresh_contents,
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            browser_btn_frame,
            text="📜 Recent Commits",
            command=self._show_commits,
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=3)

        self.contents_text = scrolledtext.ScrolledText(
            browser_frame,
            wrap=tk.WORD,
            font=("Courier", 10)
        )
        self.contents_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Activity log
        log_frame = tk.LabelFrame(
            self.root,
            text="📝 Activity Log",
            font=("Arial", 11, "bold")
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Courier", 9),
            height=6
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Status: Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 10)
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.log("✅ GitHub Uploader ready for Android")
        self.log("📱 Configure your repository settings above")
        self.log("🔑 Get your token from: github.com/settings/tokens")

    def log(self, message):
        """Add message to activity log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def _update_status(self, message, bg=None):
        """Update status bar."""
        self.status_label.config(text=f"Status: {message}")
        if bg:
            self.status_label.config(bg=bg)

    def _check_config(self):
        """Check and load existing configuration."""
        if self.api.owner:
            self.owner_entry.delete(0, tk.END)
            self.owner_entry.insert(0, self.api.owner)
        if self.api.repo:
            self.repo_entry.delete(0, tk.END)
            self.repo_entry.insert(0, self.api.repo)

    def _toggle_token_visibility(self):
        """Toggle token visibility."""
        current = self.token_entry.cget('show')
        self.token_entry.config(show='' if current == '*' else '*')

    def _update_api_config(self):
        """Update API configuration from entries."""
        self.api.token = self.token_entry.get().strip()
        self.api.owner = self.owner_entry.get().strip()
        self.api.repo = self.repo_entry.get().strip()

    def _test_connection(self):
        """Test GitHub connection."""
        self._update_api_config()

        if not self.api.token:
            messagebox.showerror("Error", "Please enter your GitHub token")
            return

        self.log("🔍 Testing connection...")
        self._update_status("Testing...", "lightyellow")

        def test():
            success, message = self.api.test_connection()
            if success:
                self.log(f"✅ {message}")
                self._update_status("Connected", "lightgreen")

                # Get repo info
                repo_info = self.api.get_repo_info()
                if 'error' not in repo_info:
                    self.log(f"📦 Repository: {repo_info.get('full_name', 'Unknown')}")
                    self.log(f"📊 Stars: {repo_info.get('stargazers_count', 0)}")
            else:
                self.log(f"❌ {message}")
                self._update_status("Connection failed", "lightcoral")
                messagebox.showerror("Connection Failed", message)

        threading.Thread(target=test, daemon=True).start()

    def _save_config(self):
        """Save configuration."""
        self._update_api_config()
        self.api.save_config()
        self.log("💾 Configuration saved (token not stored for security)")
        messagebox.showinfo("Saved", "Configuration saved!\n\nNote: Token is NOT saved for security. You'll need to enter it each time.")

    def _browse_file(self):
        """Browse for file to upload."""
        try:
            filename = filedialog.askopenfilename(
                title="Select file to upload",
                initialdir=os.path.expanduser("~")
            )
            if filename:
                self.file_entry.delete(0, tk.END)
                self.file_entry.insert(0, filename)

                # Auto-fill remote path and message
                basename = os.path.basename(filename)
                if not self.remote_entry.get():
                    self.remote_entry.insert(0, basename)
                if not self.message_entry.get():
                    self.message_entry.insert(0, f"Upload {basename}")
        except Exception as e:
            self.log(f"❌ File browser error: {e}")

    def _upload_file(self):
        """Upload selected file to GitHub."""
        self._update_api_config()

        local_path = self.file_entry.get().strip()
        remote_path = self.remote_entry.get().strip()
        message = self.message_entry.get().strip()
        branch = self.branch_entry.get().strip() or 'main'

        if not local_path:
            messagebox.showerror("Error", "Please select a file to upload")
            return

        if not os.path.exists(local_path):
            messagebox.showerror("Error", f"File not found: {local_path}")
            return

        if not message:
            message = f"Upload {os.path.basename(local_path)}"

        self.log(f"📤 Uploading: {local_path}")
        self._update_status("Uploading...", "lightyellow")

        def upload():
            result = self.api.upload_local_file(
                local_path,
                repo_path=remote_path or None,
                message=message,
                branch=branch
            )

            if 'error' in result:
                self.log(f"❌ Upload failed: {result['error']}")
                self._update_status("Upload failed", "lightcoral")
                messagebox.showerror("Upload Failed", result['error'])
            else:
                self.log(f"✅ Successfully uploaded to {remote_path or os.path.basename(local_path)}")
                self._update_status("Upload successful!", "lightgreen")
                messagebox.showinfo("Success", "File uploaded successfully!")

                # Clear entries for next upload
                self.file_entry.delete(0, tk.END)
                self.remote_entry.delete(0, tk.END)
                self.message_entry.delete(0, tk.END)

                # Refresh contents
                self._refresh_contents()

        threading.Thread(target=upload, daemon=True).start()

    def _create_new_file(self):
        """Create a new file directly in the repository."""
        self._update_api_config()

        if not self.api.token or not self.api.owner or not self.api.repo:
            messagebox.showerror("Error", "Please configure repository settings first")
            return

        # Create dialog for new file
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New File")
        dialog.geometry("600x400")

        tk.Label(
            dialog,
            text="File Path:",
            font=("Arial", 11)
        ).pack(anchor=tk.W, padx=10, pady=5)

        path_entry = tk.Entry(dialog, font=("Courier", 10), width=60)
        path_entry.pack(padx=10, fill=tk.X)

        tk.Label(
            dialog,
            text="Content:",
            font=("Arial", 11)
        ).pack(anchor=tk.W, padx=10, pady=5)

        content_text = scrolledtext.ScrolledText(dialog, font=("Courier", 10), height=12)
        content_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        tk.Label(
            dialog,
            text="Commit Message:",
            font=("Arial", 11)
        ).pack(anchor=tk.W, padx=10, pady=5)

        msg_entry = tk.Entry(dialog, font=("Courier", 10), width=60)
        msg_entry.pack(padx=10, fill=tk.X)

        def create():
            path = path_entry.get().strip()
            content = content_text.get("1.0", tk.END)
            message = msg_entry.get().strip() or f"Create {path}"
            branch = self.branch_entry.get().strip() or 'main'

            if not path:
                messagebox.showerror("Error", "Please enter a file path")
                return

            self.log(f"✏️ Creating: {path}")

            result = self.api.create_or_update_file(path, content, message, branch)

            if 'error' in result:
                self.log(f"❌ Create failed: {result['error']}")
                messagebox.showerror("Create Failed", result['error'])
            else:
                self.log(f"✅ Successfully created: {path}")
                messagebox.showinfo("Success", f"File created: {path}")
                dialog.destroy()
                self._refresh_contents()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="✅ Create File",
            command=lambda: threading.Thread(target=create, daemon=True).start(),
            bg='#2ea44f',
            fg='white',
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="❌ Cancel",
            command=dialog.destroy,
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=10)

    def _refresh_contents(self):
        """Refresh repository contents display."""
        self._update_api_config()

        if not self.api.owner or not self.api.repo:
            self.contents_text.delete("1.0", tk.END)
            self.contents_text.insert(tk.END, "Please configure repository settings first.")
            return

        self.log("🔄 Refreshing repository contents...")
        self.contents_text.delete("1.0", tk.END)
        self.contents_text.insert(tk.END, "Loading...")

        def refresh():
            contents = self.api.list_contents()

            self.contents_text.delete("1.0", tk.END)

            if 'error' in contents:
                self.contents_text.insert(tk.END, f"Error: {contents['error']}")
                return

            if isinstance(contents, list):
                self.contents_text.insert(tk.END, f"📦 {self.api.owner}/{self.api.repo}\n")
                self.contents_text.insert(tk.END, "=" * 50 + "\n\n")

                for item in contents:
                    if item.get('type') == 'dir':
                        self.contents_text.insert(tk.END, f"📁 {item.get('name', 'Unknown')}/\n")
                    else:
                        size = item.get('size', 0)
                        size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                        self.contents_text.insert(tk.END, f"📄 {item.get('name', 'Unknown')} ({size_str})\n")

                self.log("✅ Repository contents loaded")
            else:
                self.contents_text.insert(tk.END, "Unexpected response format")

        threading.Thread(target=refresh, daemon=True).start()

    def _show_commits(self):
        """Show recent commits."""
        self._update_api_config()

        if not self.api.owner or not self.api.repo:
            messagebox.showerror("Error", "Please configure repository settings first")
            return

        self.log("📜 Loading recent commits...")

        def load():
            branch = self.branch_entry.get().strip() or 'main'
            commits = self.api.get_commits(branch=branch)

            self.contents_text.delete("1.0", tk.END)

            if 'error' in commits:
                self.contents_text.insert(tk.END, f"Error: {commits['error']}")
                return

            if isinstance(commits, list):
                self.contents_text.insert(tk.END, f"📜 Recent Commits on {branch}\n")
                self.contents_text.insert(tk.END, "=" * 50 + "\n\n")

                for commit in commits:
                    sha = commit.get('sha', 'Unknown')[:7]
                    commit_data = commit.get('commit', {})
                    message = commit_data.get('message', 'No message')[:60]
                    author = commit_data.get('author', {}).get('name', 'Unknown')
                    date = commit_data.get('author', {}).get('date', '')[:10]

                    self.contents_text.insert(tk.END, f"🔹 {sha} - {message}\n")
                    self.contents_text.insert(tk.END, f"   by {author} on {date}\n\n")

                self.log("✅ Commits loaded")
            else:
                self.contents_text.insert(tk.END, "No commits found")

        threading.Thread(target=load, daemon=True).start()

    def run(self):
        """Run the application."""
        self.root.mainloop()


def cli_mode():
    """Command-line interface mode."""
    print("=" * 60)
    print("GITHUB UPLOADER - CLI MODE")
    print("For Android/Pydroid without tkinter")
    print("=" * 60)
    print()

    api = GitHubAPI()

    # Get configuration
    print("Configuration:")
    token = input("GitHub Token (paste and press Enter): ").strip()
    owner = input(f"Repository Owner [{api.owner or 'username'}]: ").strip() or api.owner
    repo = input(f"Repository Name [{api.repo or 'repo'}]: ").strip() or api.repo

    api.token = token
    api.owner = owner
    api.repo = repo

    # Test connection
    print("\nTesting connection...")
    success, message = api.test_connection()
    print(f"{'✅' if success else '❌'} {message}")

    if not success:
        return

    api.save_config()
    print("Configuration saved.")

    # Main menu
    while True:
        print("\n" + "=" * 40)
        print("Options:")
        print("1. Upload a file")
        print("2. Create new file")
        print("3. List repository contents")
        print("4. Show recent commits")
        print("5. Exit")
        print("=" * 40)

        choice = input("Select option (1-5): ").strip()

        if choice == '1':
            local_path = input("Local file path: ").strip()
            if not os.path.exists(local_path):
                print(f"❌ File not found: {local_path}")
                continue

            remote_path = input(f"Remote path [{os.path.basename(local_path)}]: ").strip()
            message = input("Commit message: ").strip()

            print("Uploading...")
            result = api.upload_local_file(
                local_path,
                repo_path=remote_path or None,
                message=message or None
            )

            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                print("✅ File uploaded successfully!")

        elif choice == '2':
            path = input("File path in repo: ").strip()
            print("Enter content (type END on a new line to finish):")
            lines = []
            while True:
                line = input()
                if line == 'END':
                    break
                lines.append(line)
            content = '\n'.join(lines)
            message = input("Commit message: ").strip()

            print("Creating file...")
            result = api.create_or_update_file(path, content, message or f"Create {path}")

            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                print("✅ File created successfully!")

        elif choice == '3':
            print("\nRepository contents:")
            contents = api.list_contents()
            if 'error' in contents:
                print(f"❌ Error: {contents['error']}")
            elif isinstance(contents, list):
                for item in contents:
                    icon = "📁" if item.get('type') == 'dir' else "📄"
                    print(f"  {icon} {item.get('name', 'Unknown')}")

        elif choice == '4':
            print("\nRecent commits:")
            commits = api.get_commits()
            if 'error' in commits:
                print(f"❌ Error: {commits['error']}")
            elif isinstance(commits, list):
                for commit in commits[:10]:
                    sha = commit.get('sha', 'Unknown')[:7]
                    message = commit.get('commit', {}).get('message', 'No message').split('\n')[0][:50]
                    print(f"  {sha}: {message}")

        elif choice == '5':
            print("Goodbye!")
            break


if __name__ == "__main__":
    print("=" * 70)
    print("GITHUB UPLOADER FOR ANDROID")
    print("Automate GitHub uploads from your Android tablet with Pydroid")
    print("By Adam Lee Hatchett")
    print("=" * 70)
    print()

    if tk:
        app = GitHubUploaderGUI()
        app.run()
    else:
        cli_mode()
