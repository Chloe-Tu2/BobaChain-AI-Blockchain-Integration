# BobaChain - Complete Setup & Run Guide

## 📦 Getting Started

This guide shows you how to download and run BobaChain locally or with Docker.

---

## Option 1: Run Locally (Recommended for Development)

### Prerequisites
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** - [Download](https://nodejs.org/)
- **Ganache CLI** - For local blockchain
- **Git** (optional) - To clone if using git

### Step 1: Extract the ZIP File

```powershell
# Right-click the zip file → Extract All
# Or use PowerShell:
Expand-Archive -Path boba-chain.zip -DestinationPath C:\Users\YourUsername\boba-chain
cd C:\Users\YourUsername\boba-chain
```

### Step 2: Install Ganache CLI (Local Blockchain)

```powershell
# Install Ganache globally
npm install -g ganache-cli

# Or if you have issues, use:
npm install -g ganache-cli@latest
```

Verify installation:
```powershell
ganache-cli --version
```

### Step 3: Start Ganache (Local Blockchain)

Open a **new PowerShell terminal** and run:

```powershell
ganache-cli --deterministic --accounts 10 --host 0.0.0.0 --port 8545
```

**Expected output:**
```
Ganache CLI v6.x.x (ganache-core: x.x.x)
...
Listening on 0.0.0.0:8545
```

Leave this running (don't close the terminal).

### Step 4: Install Backend Dependencies

Open a **new PowerShell terminal** in the project directory:

```powershell
cd C:\Users\YourUsername\boba-chain\backend
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask==2.0.1 Flask-Cors==3.0.10 web3==5.24.0 ...
```

### Step 5: (Optional) Enable Claude Haiku 4.5

If you have Claude Haiku 4.5 API key:

```powershell
# Set the API key
$env:CLAUDE_API_KEY = "sk-ant-your-key-here"

# Verify it's set
echo $env:CLAUDE_API_KEY
```

If you don't have a key, the app works fine without it (uses local summarization).

### Step 6: Start Backend Server

In the same terminal (backend directory):

```powershell
python app.py
```

**Expected output:**
```
Starting BobaChain Flask application...
 * Running on http://0.0.0.0:5000
```

Leave this running.

### Step 7: Install and Start Frontend (Optional)

Open a **new PowerShell terminal**:

```powershell
cd C:\Users\YourUsername\boba-chain\frontend
npm install
npm start
```

**Expected output:**
```
Compiled successfully!
Local: http://localhost:3000
```

---

## Option 2: Run with Docker (Recommended for Production)

### Prerequisites
- **Docker** - [Download & Install](https://www.docker.com/products/docker-desktop)
- **Docker Compose** - Usually included with Docker Desktop

### Step 1: Extract the ZIP File

```powershell
# Extract the zip file
Expand-Archive -Path boba-chain.zip -DestinationPath C:\Users\YourUsername\boba-chain
cd C:\Users\YourUsername\boba-chain
```

### Step 2: Create Environment File (Optional)

Create a `.env` file in the project root for Claude Haiku 4.5 (optional):

```bash
CLAUDE_API_KEY=sk-ant-your-key-here
CLAUDE_API_URL=https://api.anthropic.com/v1
BLOCKCHAIN_PROVIDER=http://blockchain:8545
```

If you don't have Claude API key, just skip this step.

### Step 3: Start All Services

```powershell
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**Expected output from `docker-compose ps`:**
```
NAME              STATUS
boba-blockchain   Up (healthy)
boba-backend      Up (healthy)
boba-frontend     Up
```

### Step 4: Access the Services

- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **Blockchain RPC**: http://localhost:8545

### Step 5: Stop Services

```powershell
# Stop all services
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## 🧪 Testing the API

### Test 1: Health Check

```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get | ConvertTo-Json

# Or using curl
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "blockchain_connected": true,
  "message": "API is running and connected to blockchain"
}
```

### Test 2: Check AI Configuration

```powershell
curl http://localhost:5000/api/config
```

**Response (with Claude enabled):**
```json
{
  "ai_model": "claude-3-5-haiku-20241022",
  "claude_enabled": true,
  "blockchain_connected": true
}
```

**Response (without Claude - normal):**
```json
{
  "ai_model": "local",
  "claude_enabled": false,
  "blockchain_connected": true
}
```

### Test 3: Create a Batch

```powershell
$body = @{
    name = "Tapioca Pearls"
    origin = "Taiwan"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/batch" `
    -Method Post `
    -Body $body `
    -ContentType "application/json" | ConvertTo-Json
```

**Expected response:**
```json
{
  "message": "Batch created successfully",
  "batch_id": 1,
  "name": "Tapioca Pearls",
  "origin": "Taiwan",
  "tx_hash": "0x123abc..."
}
```

### Test 4: Get All Batches

```powershell
curl http://localhost:5000/api/batches
```

### Test 5: Get AI Summary

```powershell
curl http://localhost:5000/api/summary
```

### Test 6: Run Unit Tests

```powershell
cd backend
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=.
```

---

## 📋 File Structure Reference

```
boba-chain/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Docker image definition
│   ├── pytest.ini               # Pytest configuration
│   ├── ai/
│   │   ├── assistant.py         # Claude Haiku 4.5 integration
│   │   └── utils.py
│   ├── services/
│   │   ├── blockchain.py        # Blockchain service
│   │   └── __init__.py
│   ├── models/
│   │   └── batch_model.py       # Data models
│   └── tests/
│       └── test_api.py          # API tests (40+ cases)
├── frontend/
│   ├── package.json             # Node dependencies
│   ├── Dockerfile
│   ├── index.html
│   └── src/
│       └── app.js
├── contracts/
│   └── BatchTracker.sol         # Smart contract
├── docker-compose.yml           # Docker setup
├── .env.example                 # Configuration template
├── README.md                    # Project overview
├── QUICKSTART.md               # 30-second setup
└── IMPLEMENTATION_GUIDE.md     # Technical details
```

---

## 🐛 Troubleshooting

### Problem: "Port 5000 already in use"

**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID 12345 /F
```

### Problem: "Ganache CLI not found"

**Solution:**
```powershell
# Install ganache globally
npm install -g ganache-cli@latest

# Verify
ganache-cli --version
```

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```powershell
cd backend
pip install -r requirements.txt
```

### Problem: "Cannot connect to blockchain"

**Solution:**
- Make sure Ganache is running on port 8545
- Check: `ganache-cli --deterministic --accounts 10 --host 0.0.0.0 --port 8545`

### Problem: "Docker services not starting"

**Solution:**
```powershell
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problem: "Claude API error: 401"

**Solution:**
- Verify API key: `echo $env:CLAUDE_API_KEY`
- Check key format: Should start with `sk-ant-`
- Regenerate key from console.anthropic.com if needed
- App still works without it (uses local summarization)

---

## 📊 Quick Reference Commands

### Local Development

```powershell
# Terminal 1: Ganache (Local Blockchain)
ganache-cli --deterministic --accounts 10 --host 0.0.0.0 --port 8545

# Terminal 2: Backend
cd backend
python app.py

# Terminal 3: Frontend (Optional)
cd frontend
npm install
npm start

# Terminal 4: Tests
cd backend
pytest tests/ -v
```

### Docker Deployment

```powershell
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend

# Stop everything
docker-compose down
```

### API Testing

```powershell
# Health check
curl http://localhost:5000/api/health

# Check config
curl http://localhost:5000/api/config

# Create batch
curl -X POST http://localhost:5000/api/batch `
  -H "Content-Type: application/json" `
  -d '{"name":"Tapioca Pearls","origin":"Taiwan"}'

# Get all batches
curl http://localhost:5000/api/batches

# Get summary
curl http://localhost:5000/api/summary
```

---

## 🎯 Next Steps

1. **Extract** the zip file
2. **Install** Ganache CLI: `npm install -g ganache-cli`
3. **Start** Ganache in one terminal
4. **Install** backend dependencies: `pip install -r requirements.txt`
5. **Run** backend: `python app.py`
6. **Test** API: `curl http://localhost:5000/api/health`

---

## 📚 Documentation

- **README.md** - Project overview & features
- **QUICKSTART.md** - 30-second setup
- **IMPLEMENTATION_GUIDE.md** - Technical details
- **00_START_HERE.md** - Visual guide

---

## ✅ Success Indicators

- [ ] Ganache running on port 8545
- [ ] Backend running on port 5000
- [ ] Health check returns `"status": "healthy"`
- [ ] Config endpoint shows blockchain connected
- [ ] Can create batches successfully
- [ ] Can get AI summaries

---

## 🆘 Need Help?

1. Check `README.md` for overview
2. See `QUICKSTART.md` for quick setup
3. Review `IMPLEMENTATION_GUIDE.md` for technical details
4. Check inline code comments in `backend/app.py`

---

**Ready to run BobaChain!** 🚀

Choose Option 1 (Local) for development or Option 2 (Docker) for production.
