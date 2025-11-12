# 📋 Copy-Paste Commands for GitHub Push

## ⚠️ PREREQUISITE: Install Git First

**Git is not installed on your system.** Follow these steps:

1. **Download Git**: https://git-scm.com/downloads
2. **Click Windows** (auto-detected)
3. **Run the .exe installer** and click through (all defaults are OK)
4. **Restart PowerShell** after install completes
5. **Verify**: Run `git --version` in PowerShell — you should see a version number

**Then proceed with the commands below.**

---

## 🚀 STEP-BY-STEP COMMANDS TO COPY & PASTE

---

## STEP 1: Get Your GitHub Info

### 1A. Your GitHub Token
**Instructions:**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `BobaChain-Push`
4. Check: repo, workflow
5. Generate and COPY the token

**Your token looks like**:
```
ghp_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0
```

**Save it here**:
```
MY TOKEN: _________________________________
```

---

### 1B. Your GitHub Username
**Instructions:**
1. Go to: https://github.com
2. Click your profile photo (top right)
3. Click "Your profile"
4. Copy your username from the URL

**Your username looks like**:
```
john-doe
```

**Save it here**:
```
MY USERNAME: _________________________________
```

---

### 1C. Your Repository URL

**Your actual repository URL** (already filled in for you):
```
https://github.com/Chloe-Tu2/boba-chain.git
```

**No need to change this — it's ready to use!**

---

## STEP 2: Copy-Paste These Commands

### Open PowerShell

**Windows**: Press `Windows Key + R`, type `powershell`, press Enter

Or search for PowerShell in Start Menu

---

### COMMAND 1: Navigate to Project
```powershell
cd C:\Users\cocob\boba-chain
```

**What it does**: Goes to your project folder

---

### COMMAND 2: Initialize Git
```powershell
git init
```

**What it does**: Starts tracking files with Git

---

### COMMAND 3: Add All Files
```powershell
git add .
```

**What it does**: Stages all files for upload

---

### COMMAND 4: Create Commit
```powershell
git commit -m "Initial commit: BobaChain AI + Blockchain integration"
```

**What it does**: Creates a snapshot of your code

---

### COMMAND 5: Add GitHub Repository Link

**Already filled with your repo — just copy and paste:**

```powershell
git remote add origin https://github.com/Chloe-Tu2/boba-chain.git
```

(No need to replace anything — this is your actual repo URL)

---

### COMMAND 6: Set Branch Name
```powershell
git branch -M main
```

**What it does**: Names your main branch "main"

---

### COMMAND 7: Push to GitHub
```powershell
git push -u origin main
```

**What it does**: Uploads your code to GitHub

**When prompted**:
- **Username for 'https://github.com'**: Enter your GitHub username
- **Password for 'https://...'**: Paste your token (right-click to paste in PowerShell)

---

## 📋 ALL COMMANDS AT ONCE

**BEFORE running these:** Install Git first (see prerequisites above).

After Git is installed and PowerShell is restarted, copy-paste this entire block:

```powershell
cd C:\Users\cocob\boba-chain
git init
git add .
git commit -m "Initial commit: BobaChain AI + Blockchain integration"
git remote add origin https://github.com/Chloe-Tu2/boba-chain.git
git branch -M main
git config --global credential.helper manager-core
git push -u origin main
```

**When prompted for credentials:**
- **Username**: Chloe-Tu2
- **Password**: Paste your new PAT token (NOT the old exposed one)

---

## ✅ What to See After Each Command

### After `git init`:
```
Initialized empty Git repository in C:\Users\cocob\boba-chain\.git
```
✅ Expected (no error)

### After `git add .`:
```
(no output is normal)
```
✅ Expected (silent success)

### After `git commit -m "..."`:
```
[main (root-commit) abc1234] Initial commit: BobaChain AI + Blockchain integration
 40 files changed, 1500 insertions(+)
```
✅ Expected (numbers may vary)

### After `git remote add origin https://...`:
```
(no output is normal)
```
✅ Expected (silent success)

### After `git branch -M main`:
```
(no output is normal)
```
✅ Expected (silent success)

### After `git push -u origin main`:
**You'll be prompted for credentials**:
```
Username for 'https://github.com': john-doe
Password for 'https://john-doe@github.com': ghp_...
```

**Then you'll see**:
```
Enumerating objects: 100% (50/50)
Counting objects: 100% (50/50)
Compressing objects: 100% (50/50)
Writing objects: 100% (50/50), 250.00 KiB
Pushing to 'https://github.com/john-doe/boba-chain.git'
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ SUCCESS! Your code is on GitHub!

---

## 🆘 If Something Goes Wrong

### Error: "authentication failed"
**Solution**:
- Check your token is correct (no extra spaces)
- Check token hasn't expired (create new one)
- Paste the FULL token (usually 40+ characters)

**Try again**:
```powershell
git push -u origin main
```

---

### Error: "remote origin already exists"
**Solution**:
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/boba-chain.git
git push -u origin main
```

---

### Error: "fatal: not a git repository"
**Solution**:
```powershell
cd C:\Users\cocob\boba-chain
git init
git push -u origin main
```

---

### Error: "connection refused"
**Solution**:
- Check internet connection
- Wait 30 seconds and try again
- Restart PowerShell

---

## ✨ After Success

### Your GitHub URL is:
```
https://github.com/YOUR_USERNAME/boba-chain
```

### Verify by:
1. Open: `https://github.com/YOUR_USERNAME/boba-chain`
2. You should see all your files
3. Click on `backend/`, `frontend/`, etc. to verify they uploaded

### Make Sure You See:
- ✅ backend/ folder with Python files
- ✅ frontend/ folder with HTML/JS
- ✅ contracts/ folder with Solidity
- ✅ tests/ folder
- ✅ docker-compose.yml
- ✅ README.md
- ✅ All documentation files

---

## 📝 CHECKLIST

Before pushing:
- ✅ GitHub account created
- ✅ Token generated and saved
- ✅ Repository created on GitHub
- ✅ Git is installed (check: `git --version`)

While pushing:
- ✅ Navigated to project folder
- ✅ All commands executed without error
- ✅ Entered username and token when prompted

After pushing:
- ✅ Saw "main -> main" in output
- ✅ Files visible on GitHub website
- ✅ Can access: `https://github.com/YOUR_USERNAME/boba-chain`

---

## 🎉 DONE!

Once you see your files on GitHub:

**Your submission URL is**:
```
https://github.com/YOUR_USERNAME/boba-chain
```

**Use this URL to submit your project!**

---

## 📚 FUTURE UPDATES

To push changes later:
```powershell
cd C:\Users\cocob\boba-chain
git add .
git commit -m "Describe what changed"
git push
```

No need to enter token again (credential helper will remember).

---

**Guide Created**: November 11, 2025  
**Status**: ✅ Ready to Use  
**Estimated Time**: 5-10 minutes  
**Difficulty**: Easy (copy-paste commands)
