pragma solidity ^0.8.0;

contract BatchTracker {
    struct Batch {
        string name;
        string origin;
        string[] trackingHistory;
        uint256 timestamp;
    }

    mapping(uint256 => Batch) public batches;
    uint256 public batchCount;

    event BatchCreated(uint256 batchId, string name, string origin);
    event TrackingStepAdded(uint256 batchId, string step);

    function createBatch(string memory _name, string memory _origin) public {
        batchCount++;
        batches[batchCount] = Batch(_name, _origin, new string[](0), block.timestamp);
        emit BatchCreated(batchCount, _name, _origin);
    }

    function addTrackingStep(uint256 _batchId, string memory _step) public {
        require(_batchId > 0 && _batchId <= batchCount, "Batch does not exist");
        batches[_batchId].trackingHistory.push(_step);
        emit TrackingStepAdded(_batchId, _step);
    }

    function getBatchHistory(uint256 _batchId) public view returns (Batch memory) {
        require(_batchId > 0 && _batchId <= batchCount, "Batch does not exist");
        return batches[_batchId];
    }
}