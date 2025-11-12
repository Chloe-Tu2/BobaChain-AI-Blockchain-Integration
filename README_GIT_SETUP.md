# 🚀 Git Setup & GitHub Push Guide for BobaChain

## Step 1: Install Git on Windows

### Option A: Direct Download (Recommended)
1. Go to: https://git-scm.com/download/win
2. Click **"Click here to download"** (or **"64-bit Git for Windows Setup"**)
3. Run the installer (`Git-2.x.x-64-bit.exe`)
4. **Installation Settings**:
   - Select all default options
   - Choose "Use Git from Git Bash only" or "Use Git from the Windows Command Line" (second option is better)
   - Select "Use the native Windows Secure Channel for HTTPS"
   - Choose "Checkout Windows-style, commit Unix-style line endings"

### Option B: Using Chocolatey (if installed)
```powershell
choco install git -y
```

### Option C: Using Windows Package Manager
```powershell
winget install Git.Git
```

### Verify Installation
After installation, **close and reopen PowerShell**, then run:
```powershell
git --version
```

You should see: `git version 2.x.x.windows.x`

---

## Step 2: Configure Git Locally

Run these commands once to set up your Git identity:

```powershell
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"
git config --global core.autocrlf true
```

**Verify configuration:**
```powershell
git config --global --list
```

---

## Step 3: Initialize Local Git Repository

Navigate to the project and initialize git:

```powershell
cd c:\Users\cocob\boba-chain

# Initialize repository
git init

# Verify initialization
ls -la | grep .git
```

Output should show a `.git` folder created.

---

## Step 4: Add All Files to Git

```powershell
# Add all files
git add .

# Check status (shows files staged for commit)
git status
```

### Verify Files Are Staged
You should see "Changes to be committed:" followed by all your files (green color in terminal).

---

## Step 5: Create Initial Commit

```powershell
git commit -m "Initial commit: BobaChain - AI + Blockchain supply chain application

- Blockchain integration with Ganache and Web3.py
- Claude Haiku 4.5 AI integration for supply chain analysis
- REST API with 7 endpoints for batch management
- 40+ unit tests with full coverage
- Docker Compose setup for production deployment
- Smart contracts for on-chain batch tracking
- Comprehensive documentation and deployment guides"
```

**Verify commit:**
```powershell
git log
```

You should see your commit message and author info.

---

## Step 6: Create GitHub Repository

### Option A: Via GitHub Web (Recommended for Control)

1. Go to: https://github.com/new
2. Fill in details:
   - **Repository name**: `boba-chain` (or your preferred name)
   - **Description**: "AI + Blockchain Supply Chain Application"
   - **Visibility**: Choose "Public" (for submission) or "Private"
   - **Do NOT** initialize with README, .gitignore, or license (we already have files)
3. Click **"Create repository"**
4. You'll see a page with commands. Note the repository URL (either HTTPS or SSH)

### Option B: Via GitHub CLI (if installed)

```powershell
# Ensure you're logged in
gh auth login

# Create new repository
gh repo create boba-chain --public --description "AI + Blockchain Supply Chain Application" --source=. --remote=origin --push
```

---

## Step 7: Add Remote and Push (HTTPS Method)

If you chose HTTPS on GitHub, use these commands:

```powershell
cd c:\Users\cocob\boba-chain

# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/boba-chain.git

# Verify remote was added
git remote -v
```

**Output should show**:
```
origin  https://github.com/YOUR_USERNAME/boba-chain.git (fetch)
origin  https://github.com/YOUR_USERNAME/boba-chain.git (push)
```

### Push to GitHub

```powershell
# Push main branch
git branch -M main
git push -u origin main
```

**First time prompt**: GitHub will ask for authentication
- Enter your GitHub username
- For password, use a **Personal Access Token (PAT)** instead of your actual password

### Creating a Personal Access Token (PAT)

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Enter token name: "BobaChain Push"
4. Select scopes: `repo` (full control of private repositories)
5. Click **"Generate token"**
6. **COPY the token** (you won't see it again!)
7. Use this token as the password when prompted by git

---

## Step 8: Add Remote and Push (SSH Method - Optional)

If you prefer SSH (requires setup but no password prompts):

### Generate SSH Key (if you don't have one)

```powershell
# Generate key (press Enter to accept defaults)
ssh-keygen -t ed25519 -C "your.email@example.com"

# List keys (verify it was created)
ls ~/.ssh/
```

### Add SSH Key to GitHub

1. Copy your public key:
```powershell
cat ~/.ssh/id_ed25519.pub
```

2. Go to: https://github.com/settings/keys
3. Click **"New SSH key"**
4. Paste the key, give it a name
5. Click **"Add SSH key"**

### Push via SSH

```powershell
cd c:\Users\cocob\boba-chain

# Add remote with SSH URL
git remote add origin git@github.com:YOUR_USERNAME/boba-chain.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 9: Verify Push Success

### On GitHub Web
1. Go to: https://github.com/YOUR_USERNAME/boba-chain
2. You should see all your files and folders
3. Check the commit history (click "X commits")

### In PowerShell
```powershell
# Verify remote tracking
git branch -vv
```

Output should show: `main 1234567 [origin/main] Initial commit: ...`

---

## Step 10: Push Tags and Additional Branches (Optional)

```powershell
# Tag the initial release
git tag -a v1.0.0 -m "Initial BobaChain release - Production ready"

# Push tags to GitHub
git push origin --tags

# Push all branches (if you have multiple)
git push --all origin
```

---

## Complete Workflow Summary

```powershell
# 1. Install Git (one-time setup)
#    Download from git-scm.com or use chocolatey

# 2. Configure Git (one-time)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 3. Initialize repository
cd c:\Users\cocob\boba-chain
git init
git add .
git commit -m "Initial commit: BobaChain project"

# 4. Create repo on GitHub (via web interface)
#    https://github.com/new

# 5. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/boba-chain.git
git branch -M main
git push -u origin main

# 6. (Optional) Add tags
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin --tags
```

---

## Troubleshooting

### Error: "git: The term 'git' is not recognized"
**Solution**: Git not installed or PATH not updated. Restart PowerShell after installation.

### Error: "fatal: not a git repository"
**Solution**: Run `git init` in your project directory first.

### Error: "fatal: could not read from remote repository"
**Solution**: Check your remote URL with `git remote -v`. Ensure it's correct and you have network access.

### Error: "Permission denied (publickey)" (SSH only)
**Solution**: Your SSH key isn't registered. Follow SSH setup section or use HTTPS instead.

### Error: "fatal: 'origin' does not appear to be a 'git' repository"
**Solution**: Remove old remote and add new one:
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/boba-chain.git
```

### Large file warning
If you see warnings about large files, create `.gitignore`:
```powershell
# Create .gitignore in project root
$ignore = @"
__pycache__/
*.pyc
*.pyo
node_modules/
.env
.DS_Store
*.zip
"@
Set-Content -Path .gitignore -Value $ignore -Encoding UTF8

# Add and commit
git add .gitignore
git commit -m "Add .gitignore"
```

---

## Push to Existing Repository

If you already have a GitHub repository:

```powershell
cd c:\Users\cocob\boba-chain

# Check current remote
git remote -v

# If remote exists but is wrong, update it
git remote set-url origin https://github.com/YOUR_USERNAME/your-repo.git

# Push your commits
git push -u origin main
```

---

## Final Verification

After push completes, verify on GitHub:

1. **Repository Page**: https://github.com/YOUR_USERNAME/boba-chain
   - [ ] All files visible
   - [ ] Folder structure intact (backend/, frontend/, contracts/)
   - [ ] Documentation files present (README.md, SUBMISSION.md, etc.)
   - [ ] No sensitive files (like .env with real API keys)

2. **Commit History**: Click "X commits" in GitHub
   - [ ] See your initial commit
   - [ ] Check commit message

3. **Code Quality Check**: Navigate to main Python files
   - [ ] backend/app.py visible
   - [ ] backend/ai/assistant.py visible
   - [ ] backend/services/blockchain.py visible

---

## Quick Reference Commands

```powershell
# Check git status
git status

# View recent commits
git log --oneline -10

# Add specific file
git add backend/app.py

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull from GitHub
git pull

# Check remote
git remote -v

# Create and push new branch
git checkout -b new-feature
git push -u origin new-feature

# View branches
git branch -a
```

---

## Next Steps After Push

1. ✅ Verify repository on GitHub
2. ✅ Create a `README.md` on GitHub (already in repo)
3. ✅ Add GitHub URL to your assignment submission
4. ✅ (Optional) Enable GitHub Pages for documentation
5. ✅ (Optional) Set up GitHub Actions for CI/CD

---

## GitHub Repository URL Format

Once pushed, your repository will be at:
```
https://github.com/YOUR_USERNAME/boba-chain
```

Share this URL in your assignment submission! ✅

---

**Installation & Push Process**: ~10 minutes  
**Difficulty Level**: Beginner-Friendly  
**Status**: Ready for Submission ✅
