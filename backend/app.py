"""
Main Flask application for the BobaChain backend.
Provides REST API endpoints for batch management and blockchain interactions.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from models.batch_model import Batch
from ai.assistant import generate_summary
from services.blockchain import BlockchainService
import logging
from typing import Dict, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize the blockchain service
try:
    blockchain_service = BlockchainService(provider_url='http://localhost:8545')
    logger.info("Blockchain service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize blockchain service: {str(e)}")
    blockchain_service = None


# Utility functions for validation and error handling

def validate_batch_creation_data(data: Dict) -> Tuple[bool, str]:
    """
    Validate batch creation request data.

    :param data: The request data to validate
    :return: Tuple of (is_valid, error_message)
    """
    if not data:
        return False, "Request body is required"
    
    if 'name' not in data or not data['name']:
        return False, "Batch name is required and cannot be empty"
    
    if 'origin' not in data or not data['origin']:
        return False, "Batch origin is required and cannot be empty"
    
    if len(data['name']) > 255:
        return False, "Batch name cannot exceed 255 characters"
    
    if len(data['origin']) > 255:
        return False, "Batch origin cannot exceed 255 characters"
    
    return True, ""


def validate_batch_id(batch_id: str) -> Tuple[bool, str]:
    """
    Validate batch ID.

    :param batch_id: The batch ID to validate
    :return: Tuple of (is_valid, error_message)
    """
    try:
        batch_id_int = int(batch_id)
        if batch_id_int <= 0:
            return False, "Batch ID must be a positive integer"
        return True, ""
    except ValueError:
        return False, "Batch ID must be a valid integer"


def validate_tracking_step(step: str) -> Tuple[bool, str]:
    """
    Validate tracking step data.

    :param step: The tracking step to validate
    :return: Tuple of (is_valid, error_message)
    """
    if not step or not isinstance(step, str):
        return False, "Tracking step must be a non-empty string"
    
    if len(step) > 255:
        return False, "Tracking step cannot exceed 255 characters"
    
    return True, ""


# Health check endpoint

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running and blockchain is connected.

    :return: JSON response with health status
    """
    blockchain_connected = blockchain_service.is_connected() if blockchain_service else False
    
    return jsonify({
        "status": "healthy" if blockchain_connected else "degraded",
        "blockchain_connected": blockchain_connected,
        "message": "API is running" + (" and connected to blockchain" if blockchain_connected else " but blockchain connection failed")
    }), 200 if blockchain_connected else 503


# Configuration endpoint

@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get API configuration (e.g., AI model being used).
    Useful for frontend to know what AI model is active.

    :return: JSON response with configuration
    """
    from ai.assistant import CLAUDE_API_KEY, CLAUDE_MODEL
    
    ai_model = CLAUDE_MODEL if CLAUDE_API_KEY else "local"
    
    return jsonify({
        "ai_model": ai_model,
        "claude_enabled": bool(CLAUDE_API_KEY),
        "blockchain_connected": blockchain_service.is_connected() if blockchain_service else False
    }), 200


# Batch management endpoints

@app.route('/api/batch', methods=['POST'])
def create_batch():
    """
    Create a new batch on the blockchain.

    Expected JSON body:
    {
        "name": "Batch Name",
        "origin": "Origin Location"
    }

    :return: JSON response with batch creation result
    """
    try:
        # Validate blockchain service
        if not blockchain_service:
            return jsonify({"error": "Blockchain service not available"}), 503
        
        if not blockchain_service.is_connected():
            return jsonify({"error": "Not connected to blockchain"}), 503

        # Get and validate request data
        data = request.get_json()
        is_valid, error_msg = validate_batch_creation_data(data)
        
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Create batch on blockchain
        tx_hash = blockchain_service.create_batch(
            name=data['name'],
            origin=data['origin']
        )

        if not tx_hash:
            return jsonify({"error": "Failed to create batch on blockchain"}), 500

        # Get the batch ID (approximate - would need to listen to events in production)
        batch_count = blockchain_service.get_batch_count()

        return jsonify({
            "message": "Batch created successfully",
            "batch_id": batch_count,
            "name": data['name'],
            "origin": data['origin'],
            "tx_hash": tx_hash
        }), 201

    except Exception as e:
        logger.error(f"Error creating batch: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route('/api/batch/<batch_id>', methods=['GET'])
def get_batch(batch_id):
    """
    Retrieve batch information from the blockchain.

    :param batch_id: The ID of the batch to retrieve
    :return: JSON response with batch information
    """
    try:
        # Validate blockchain service
        if not blockchain_service:
            return jsonify({"error": "Blockchain service not available"}), 503
        
        if not blockchain_service.is_connected():
            return jsonify({"error": "Not connected to blockchain"}), 503

        # Validate batch ID
        is_valid, error_msg = validate_batch_id(batch_id)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Retrieve batch from blockchain
        batch_data = blockchain_service.get_batch(int(batch_id))

        if not batch_data:
            return jsonify({"error": f"Batch with ID {batch_id} not found"}), 404

        return jsonify(batch_data), 200

    except Exception as e:
        logger.error(f"Error retrieving batch {batch_id}: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route('/api/batch/<batch_id>/tracking', methods=['POST'])
def add_tracking_step(batch_id):
    """
    Add a tracking step to a batch on the blockchain.

    Expected JSON body:
    {
        "step": "Tracking step description"
    }

    :param batch_id: The ID of the batch
    :return: JSON response with result
    """
    try:
        # Validate blockchain service
        if not blockchain_service:
            return jsonify({"error": "Blockchain service not available"}), 503
        
        if not blockchain_service.is_connected():
            return jsonify({"error": "Not connected to blockchain"}), 503

        # Validate batch ID
        is_valid, error_msg = validate_batch_id(batch_id)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Get and validate tracking step
        data = request.get_json()
        if not data or 'step' not in data:
            return jsonify({"error": "Tracking step is required"}), 400

        is_valid, error_msg = validate_tracking_step(data['step'])
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Add tracking step to blockchain
        tx_hash = blockchain_service.add_tracking_step(
            batch_id=int(batch_id),
            step=data['step']
        )

        if not tx_hash:
            return jsonify({"error": "Failed to add tracking step"}), 500

        return jsonify({
            "message": "Tracking step added successfully",
            "batch_id": batch_id,
            "step": data['step'],
            "tx_hash": tx_hash
        }), 201

    except Exception as e:
        logger.error(f"Error adding tracking step: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route('/api/batches', methods=['GET'])
def get_all_batches():
    """
    Retrieve all batches from the blockchain.

    :return: JSON response with list of batches
    """
    try:
        # Validate blockchain service
        if not blockchain_service:
            return jsonify({"error": "Blockchain service not available"}), 503
        
        if not blockchain_service.is_connected():
            return jsonify({"error": "Not connected to blockchain"}), 503

        # Retrieve all batches
        batches = blockchain_service.get_all_batches()

        if batches is None:
            return jsonify({"error": "Failed to retrieve batches"}), 500

        return jsonify({
            "batches": batches,
            "count": len(batches)
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving all batches: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# AI Summary endpoint

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """
    Get an AI-generated summary of all blockchain data.

    :return: JSON response with summary
    """
    try:
        # Validate blockchain service
        if not blockchain_service:
            return jsonify({"error": "Blockchain service not available"}), 503
        
        if not blockchain_service.is_connected():
            return jsonify({"error": "Not connected to blockchain"}), 503

        # Retrieve all batches
        batches = blockchain_service.get_all_batches()

        if batches is None:
            return jsonify({"error": "Failed to retrieve batches"}), 500

        # Format data for AI summary
        raw_data = {
            'batches': [
                {
                    'id': batch['id'],
                    'name': batch['name'],
                    'origin': batch['origin'],
                    'tracking_history': batch['tracking_history']
                }
                for batch in batches
            ]
        }

        # Generate summary
        summary = generate_summary(raw_data)

        return jsonify({
            "summary": summary,
            "batch_count": len(batches)
        }), 200

    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    logger.info("Starting BobaChain Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)