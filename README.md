# BobaChain

BobaChain is a decentralized application that verifies the supply chain of boba ingredients using blockchain technology. This project integrates AI to provide insights and summaries of the blockchain data, ensuring transparency and traceability in the sourcing of boba ingredients.

## Features

- ✅ **Blockchain Integration**: Real-time batch tracking on Ethereum blockchain
- ✅ **REST API**: Complete CRUD operations for batch management
- ✅ **Input Validation**: Comprehensive validation for all endpoints
- ✅ **Error Handling**: Robust error handling and logging throughout the application
- ✅ **AI Summaries**: AI-generated summaries of blockchain data
- ✅ **Unit Tests**: Comprehensive test suite with pytest
- ✅ **Docker Deployment**: Full Docker Compose setup for easy deployment
- ✅ **Health Checks**: Built-in health check endpoints

## Project Structure

```
boba-chain
├── backend                # Backend application using Flask
│   ├── app.py            # Main entry point for the Flask application
│   ├── requirements.txt   # Python dependencies for the backend
│   ├── Dockerfile         # Docker instructions for the backend
│   ├── pytest.ini         # Pytest configuration
│   ├── ai                 # AI components for data processing
│   │   ├── assistant.py   # Logic for interacting with the LLM
│   │   └── utils.py       # Utility functions for AI processing
│   ├── models             # Data models for the application
│   │   └── batch_model.py # Model for boba ingredient batches
│   ├── services           # Service layer for business logic
│   │   ├── __init__.py    # Package initialization
│   │   └── blockchain.py  # Blockchain interaction service
│   └── tests              # Unit tests for the backend
│       ├── __init__.py    # Test package initialization
│       └── test_api.py    # Tests for API endpoints
├── contracts              # Smart contracts for the blockchain
│   ├── BatchTracker.sol   # Solidity contract for batch tracking
│   └── migrations         # Migration scripts for deploying contracts
│       └── 1_deploy_contracts.js
├── scripts                # Scripts for deployment and local testing
│   ├── deploy_contract.py  # Script to deploy the smart contract
│   └── run_local_chain.sh  # Shell script to run a local blockchain
├── frontend               # Frontend application
│   ├── Dockerfile         # Docker instructions for the frontend
│   ├── index.html         # Main HTML file for the UI
│   ├── package.json       # Frontend dependencies and scripts
│   ├── src                # Source files for the frontend
│   │   └── app.js         # JavaScript code for user interactions
├── docker-compose.yml      # Docker Compose configuration
└── README.md              # Project documentation
```

## Setup Instructions

### Option 1: Local Setup (Development)

#### Prerequisites
- Python 3.9+
- Node.js 14+
- Ganache CLI (for local blockchain)
- npm or yarn

#### Backend Setup
```powershell
cd backend
pip install -r requirements.txt
python app.py
```

#### Run Tests
```powershell
cd backend
pytest tests/ -v --cov=.
```

#### Frontend Setup
```powershell
cd frontend
npm install
npm start
```

### Option 2: Docker Deployment (Production/Easy Setup)

#### Prerequisites
- Docker
- Docker Compose

#### Configure Environment Variables (Optional - for Claude Haiku 4.5)

Create a `.env` file in the project root:

```bash
# Claude Haiku 4.5 API Configuration
CLAUDE_API_KEY=sk-ant-your-api-key-here
CLAUDE_API_URL=https://api.anthropic.com/v1

# Optional: Custom blockchain account
BLOCKCHAIN_FROM_ADDRESS=0x...
BLOCKCHAIN_PRIVATE_KEY=0x...
```

See `.env.example` for all available configuration options.

#### Deploy with Docker Compose
```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Check service status
docker-compose ps

# Stop all services
docker-compose down
```

The services will be available at:
- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **Blockchain RPC**: http://localhost:8545

## API Endpoints

### Health Check
```bash
GET /api/health
```
Response:
```json
{
  "status": "healthy",
  "blockchain_connected": true,
  "message": "API is running and connected to blockchain"
}
```

### Configuration
```bash
GET /api/config
```
Response:
```json
{
  "ai_model": "claude-3-5-haiku-20241022",
  "claude_enabled": true,
  "blockchain_connected": true
}
```

### Create Batch
```bash
POST /api/batch
Content-Type: application/json

{
  "name": "Tapioca Pearls",
  "origin": "Taiwan"
}
```
Response:
```json
{
  "message": "Batch created successfully",
  "batch_id": 1,
  "name": "Tapioca Pearls",
  "origin": "Taiwan",
  "tx_hash": "0x123abc..."
}
```

### Get Batch by ID
```bash
GET /api/batch/1
```
Response:
```json
{
  "id": 1,
  "name": "Tapioca Pearls",
  "origin": "Taiwan",
  "tracking_history": ["Harvested", "Processed"],
  "timestamp": 1234567890
}
```

### Add Tracking Step
```bash
POST /api/batch/1/tracking
Content-Type: application/json

{
  "step": "Harvested"
}
```

### Get All Batches
```bash
GET /api/batches
```
Response:
```json
{
  "batches": [...],
  "count": 2
}
```

### Get Summary
```bash
GET /api/summary
```
Response:
```json
{
  "summary": "Batch ID: 1\nName: Tapioca Pearls...",
  "batch_count": 1
}
```

## Testing

### Run All Tests
```powershell
cd backend
pytest tests/ -v
```

### Run Tests with Coverage
```powershell
pytest tests/ -v --cov=. --cov-report=html
```

### Run Specific Test Class
```powershell
pytest tests/test_api.py::TestCreateBatch -v
```

### Run Tests with Specific Markers
```powershell
pytest tests/ -m unit -v
```

## Validation & Error Handling

### Input Validation
- Batch name: Required, max 255 characters
- Batch origin: Required, max 255 characters
- Batch ID: Must be a positive integer
- Tracking step: Required, max 255 characters

### Error Responses
```json
{
  "error": "Batch name is required and cannot be empty"
}
```

HTTP Status Codes:
- **200**: Success (GET requests)
- **201**: Created (POST requests)
- **400**: Bad Request (validation error)
- **403**: Forbidden
- **404**: Not Found
- **500**: Internal Server Error
- **503**: Service Unavailable (blockchain disconnected)

## Blockchain Integration

### Smart Contract: BatchTracker

The `BatchTracker` smart contract provides:
- `createBatch(name, origin)`: Create a new batch
- `addTrackingStep(batchId, step)`: Add a tracking step
- `getBatchHistory(batchId)`: Retrieve batch information
- `batchCount`: Get total number of batches

### BlockchainService

The `BlockchainService` class handles:
- Web3 connection management
- Contract interaction
- Transaction signing and sending
- Data retrieval and formatting

## AI Integration

### Claude Haiku 4.5 Setup

BobaChain integrates with **Claude Haiku 4.5** for AI-powered supply chain analysis and summaries. 

#### Enable Claude Haiku 4.5:

1. **Get an API Key**
   - Visit [Anthropic Console](https://console.anthropic.com)
   - Create an account or sign in
   - Generate an API key

2. **Configure Environment**
   
   **Local Development:**
   ```bash
   export CLAUDE_API_KEY=sk-ant-your-key-here
   export CLAUDE_API_URL=https://api.anthropic.com/v1
   python backend/app.py
   ```
   
   **Docker Deployment:**
   Create `.env` file:
   ```bash
   CLAUDE_API_KEY=sk-ant-your-key-here
   CLAUDE_API_URL=https://api.anthropic.com/v1
   ```
   
   Then run:
   ```bash
   docker-compose up -d
   ```

3. **Verify Integration**
   ```bash
   curl http://localhost:5000/api/config
   ```
   
   Response should show:
   ```json
   {
     "ai_model": "claude-3-5-haiku-20241022",
     "claude_enabled": true,
     "blockchain_connected": true
   }
   ```

#### AI Features:

- **Auto Summary Generation**: Call `/api/summary` to get AI-generated supply chain insights
- **Fallback**: If API key not set or Claude fails, system falls back to local text summarization
- **Format**: Claude generates professional 2-3 paragraph summaries including:
  - Batch overview and origins
  - Tracking milestones
  - Supply chain patterns
  - Optimization recommendations

#### Costs & Limits:

- Claude Haiku 4.5 is the most affordable model ($0.80/$4 per 1M input/output tokens)
- No rate limits for typical supply chain queries
- See [pricing](https://www.anthropic.com/pricing) for current rates

---

## Development

### Project Structure
- **Services Layer** (`backend/services/`): Handles blockchain interactions
- **Models Layer** (`backend/models/`): Data models for the application
- **AI Layer** (`backend/ai/`): AI and summary generation
- **API Layer** (`backend/app.py`): Flask routes and validation

### Adding New Endpoints

1. Create validation function (if needed)
2. Add route handler in `app.py`
3. Add tests in `backend/tests/test_api.py`
4. Test with pytest
5. Document in README

### Logging

Logging is configured throughout the application:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Information message")
logger.error("Error message")
```

## Troubleshooting

### Blockchain Connection Issues
```
Error: "Not connected to blockchain"
```
- Ensure Ganache or local blockchain is running on port 8545
- Check blockchain service initialization in logs

### Tests Failing
```
pytest tests/ -v --tb=short
```
- Use `-v` for verbose output
- Use `--tb=short` for concise error traces
- Check mock objects are properly configured

### Docker Issues
```
# View detailed logs
docker-compose logs blockchain
docker-compose logs backend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Components

- **Backend**: Built with Flask, handles API requests and blockchain integration
- **Blockchain**: Smart contracts written in Solidity manage batch tracking
- **AI**: Generates insights and summaries of blockchain data
- **Frontend**: User-friendly interface for application interaction
- **Database**: Blockchain serves as the distributed ledger

## Performance Considerations

- Batch operations are limited by blockchain confirmation time (~15 seconds per transaction)
- API responses cached where appropriate
- Connection pooling for blockchain interactions
- Async operations for long-running tasks (future enhancement)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.