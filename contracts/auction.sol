// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Auction {
    // The address of the auction's beneficiary (the seller)
    address payable public beneficiary;

    // The timestamp when the auction ends
    uint public auctionEndTime;

    // The address of the highest bidder
    address public highestBidder;

    // The highest bid amount (in wei)
    uint public highestBid;

    // Mapping to track the funds that need to be returned to bidders
    mapping(address => uint) pendingReturns;

    // Flag to indicate whether the auction has ended
    bool public ended = false;

    // Event emitted when the highest bid is increased
    event HighestBidIncreased(address bidder, uint amount);

    // Event emitted when the auction ends
    event AuctionEnded(address winner, uint amount);

    /**
     * @dev Constructor to initialize the auction.
     * @param _biddingTime The duration (in seconds) for which the auction will run.
     * @param _beneficiary The address of the auction's beneficiary.
     */
    constructor(uint _biddingTime, address payable _beneficiary) {
        beneficiary = _beneficiary;
        auctionEndTime = block.timestamp + _biddingTime;
    }

    /**
     * @dev Function to place a bid in the auction.
     * The bid must be higher than the current highest bid.
     * Reverts if the auction has already ended or the bid is not higher.
     */
    function bid() external payable {
        // Ensure the auction is still ongoing
        require(block.timestamp <= auctionEndTime, "Auction already ended.");

        // Ensure the bid is higher than the current highest bid
        require(msg.value > highestBid, "There already is a higher bid.");

        // If there's already a bid, refund the previous highest bidder
        if (highestBid != 0) {
            pendingReturns[highestBidder] += highestBid;
        }

        // Update the highest bid and bidder
        highestBidder = msg.sender;
        highestBid = msg.value;

        // Emit an event indicating that the highest bid has increased
        emit HighestBidIncreased(msg.sender, msg.value);
    }

    /**
     * @dev Withdraws the previous bid of the caller if they have been outbid.
     * @return success Boolean indicating whether the withdrawal was successful.
     */
    function withdraw() public returns (bool success) {
        uint amount = pendingReturns[msg.sender];

        // Check if there are funds to withdraw
        if (amount > 0) {
            // Reset the pending return before transferring to prevent re-entrancy attacks
            pendingReturns[msg.sender] = 0;

            // Attempt to send the funds back to the caller
            if (!payable(msg.sender).send(amount)) {
                // If the transfer fails, restore the pending return balance
                pendingReturns[msg.sender] = amount;
                return false;
            }
        }
        return true;
    }

    /**
     * @dev Ends the auction and transfers the highest bid to the beneficiary.
     * Can only be called after the auction end time has passed.
     */
    function auctionEnd() public {
        // Ensure the auction has ended
        require(block.timestamp >= auctionEndTime, "Auction not yet ended.");

        // Ensure this function has not already been called
        require(!ended, "auctionEnd has already been called.");

        // Mark the auction as ended
        ended = true;

        // Emit an event indicating the auction has ended
        emit AuctionEnded(highestBidder, highestBid);

        // Transfer the highest bid to the beneficiary
        beneficiary.transfer(highestBid);
    }
}
