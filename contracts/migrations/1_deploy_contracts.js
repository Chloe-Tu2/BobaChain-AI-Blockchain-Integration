const BatchTracker = artifacts.require("BatchTracker");

module.exports = function (deployer) {
  deployer.deploy(BatchTracker);
};