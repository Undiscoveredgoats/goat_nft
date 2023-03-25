// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
// import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/draft-EIP712.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/draft-ERC721Votes.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract goats_nft is
    ERC721,
    ERC721URIStorage,
    Ownable,
    EIP712,
    ERC721Votes,
    VRFConsumerBaseV2
{
    //v2 shit
    bytes32 keyHash;
    VRFCoordinatorV2Interface COORDINATOR;
    uint64 s_subscriptionId;
    uint32 callbackGasLimit = 2500000;
    uint16 requestConfirmations = 3;
    uint32 numWords = 2;
    uint256[] public s_randomWords;
    uint256 mintFee;
    uint256 fee; //v1 shit
    uint256 public recent_randomness;
    uint256 public requestId;
    // contracts varibles
    uint256 public tokenCounter;
    string[5] breed = ["goat", "grind", "jump", "kompyuta", "mbuzi_head"];
    // mapping(uint256 => address) public tokenIdToAddress;
    mapping(uint256 => string) public TokenIdToBreed;
    mapping(uint256 => address) requestIdtoTokenOwner;
    event requestedNft(uint256 indexed requestId, address requester);
    event breedAssigned(string indexed breed, uint256);
    // event TokenMinted(uint256 token_id, address indexed owner);
    event UriSet(uint256 token_id, string indexed uri);
    event amountWithdrawn(address indexed withdrawer, uint256 amount);
    error GoatNft__notEnoughBalance();

    constructor(
        string memory _name,
        string memory _symbol,
        address _vrfCoordinator,
        bytes32 _keyHash,
        uint64 sId,
        uint256 _fee
    )
        ERC721(_name, _symbol)
        EIP712(_name, "1")
        VRFConsumerBaseV2(_vrfCoordinator)
    {
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        keyHash = _keyHash;
        s_subscriptionId = sId;
        mintFee = _fee;
    }

    function createGoat() public payable returns (uint256) {
        if (msg.value < mintFee) {
            revert GoatNft__notEnoughBalance();
        }
        address owner = msg.sender;
        requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        //requestId = requestRandomness(keyHash, fee);
        requestIdtoTokenOwner[requestId] = owner;
        emit requestedNft(requestId, owner);
        return requestId;
    }

    function fulfillRandomWords(
        uint256 /* requestId */,
        uint256[] memory randomWords
    ) internal override {
        s_randomWords = randomWords;
        recent_randomness = s_randomWords[0];
        string memory chosenBreed = breed[recent_randomness % 3];
        uint256 tokenId = tokenCounter;
        address owner = requestIdtoTokenOwner[requestId];
        _safeMint(owner, tokenId);
        tokenCounter++;
        TokenIdToBreed[tokenId] = chosenBreed;
        emit breedAssigned(chosenBreed, tokenId);
    }

    function setTokenUri(uint256 tokenId, string memory uri) public onlyOwner {
        _setTokenURI(tokenId, uri);
        emit UriSet(tokenId, uri);
    }

    // function pause() public onlyOwner {
    //     _pause();
    // }

    // function unpause() public onlyOwner {
    //     _unpause();
    // }

    function _afterTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override(ERC721, ERC721Votes) {
        super._afterTokenTransfer(from, to, tokenId, batchSize);
    }

    // The following functions are overrides required by Solidity.

    // function _afterTokenTransfer(
    //     address from,
    //     address to,
    //     uint256 tokenId,
    //     uint256 batchSize
    // ) internal override(ERC721, ERC721Votes) {
    //     super._afterTokenTransfer(from, to, tokenId, batchSize);
    // }

    function _burn(
        uint256 tokenId
    ) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(
        uint256 tokenId
    ) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function withdraw(uint256 _amount) public onlyOwner {
        require(
            _amount <= address(this).balance,
            "Amount is more than the contracts balance"
        );
        address payable owner = payable(msg.sender);
        owner.transfer(_amount);
        emit amountWithdrawn(owner, _amount);
    }

    function getBreed(uint256 breedIndex) public view returns (string memory) {
        return breed[breedIndex];
    }
}
