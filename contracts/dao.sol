// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DAO {
    struct Proposal {
        string title;
        string description;
        address proposer;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 endTime;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    mapping(address => bool) public voted;
    mapping(uint256 => mapping(address => bool)) public hasVoted;

    event ProposalCreated(uint256 proposalId, string title, address proposer);
    event Voted(uint256 proposalId, address voter, bool voteFor);
    event ProposalExecuted(uint256 proposalId, bool passed);

    modifier onlyBeforeEnd(uint256 _proposalId) {
        require(
            block.timestamp < proposals[_proposalId].endTime,
            "Voting period over"
        );
        _;
    }

    modifier onlyAfterEnd(uint256 _proposalId) {
        require(
            block.timestamp >= proposals[_proposalId].endTime,
            "Voting period not over"
        );
        _;
    }

    function propose(string memory _title, string memory _description) public {
        proposals[proposalCount] = Proposal({
            title: _title,
            description: _description,
            proposer: msg.sender,
            votesFor: 0,
            votesAgainst: 0,
            endTime: block.timestamp + 1 days, // Voting ends in 1 day
            executed: false
        });

        emit ProposalCreated(proposalCount, _title, msg.sender);
        proposalCount++;
    }

    function vote(
        uint256 _proposalId,
        bool _voteFor
    ) public onlyBeforeEnd(_proposalId) {
        require(
            !hasVoted[_proposalId][msg.sender],
            "You have already voted on this proposal"
        );

        if (_voteFor) {
            proposals[_proposalId].votesFor++;
        } else {
            proposals[_proposalId].votesAgainst++;
        }

        hasVoted[_proposalId][msg.sender] = true;
        emit Voted(_proposalId, msg.sender, _voteFor);
    }

    function executeProposal(
        uint256 _proposalId
    ) public onlyAfterEnd(_proposalId) {
        Proposal storage proposal = proposals[_proposalId];
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;
        bool passed = proposal.votesFor > proposal.votesAgainst;
        emit ProposalExecuted(_proposalId, passed);
    }
}
