# goat_nft

# UNDISCOVERED GOATS DAO
## CORE VALUES
The core value of UG is sustainability, digital art/film making and decentralization. Community of digital creators in the metaverse industry participants supported by infrastructure that gives them an advantage in the metaverse industry. The goal is to attract developers, VCs, founders, investors, 3d artists,filmakers and influencers who are focused on building and creating visual stories in the space.The second goal is to use our infrastructure for foundational building that gives the people a huge advantage in this industry.

## WHAT WE DO
We aim to use the power of community and web3 to create a new way were digital artist focused on web3 can build and use the technology to solve problems that digital artist encounter, while at the same time creating a community of digital artist focused on building longterm in the industry.

## BUSINESS PROCESS
The creation and immediate infrastructure is laid out by creating a more detailed work through on how the ideation and onboarding will begin, we aim to stay in the industry for the long term so we value organic growth of our community at far most, we believe in laying strong foundations that will withstand the test of time in this chaotic and unpredictable market. Some of this infrastructure may be for example UG GOAT NFT collection which will lay the foundation of what were trying to create and achieve in the UG DAO.

## VALUE PROPOSITION
**ARTIST**
<!-- ![UG dao Organization](https://github.com/Undiscoveredgoats/goats_nft/blob/main/img/artist.png). -->
<!-- https://github.com/Undiscoveredgoats/goats_nft/blob/main/img/companies.png -->
1. A hub for digital creatives in the space to meet and collaborate in building web3 art community and usher a new infrastructure for visual art in the
space.
2. A hub for artist to meet and share there knowledge on different techniques via tutorials, workshops etc
3. Branding opportunities for digital artists within the DAO.


**COMPANIES**
<!-- <p align = "left"> <img src = "https://github.com/Undiscoveredgoats/goats_nft/blob/main/img/companies.png" width = "100" height = "50"/> </p> -->

1. Partnership for branding purpose
2. Integration with different Daos that align with core values and mission


**COMMUNITY**

<!-- ![UG dao Organization](https://github.com/Undiscoveredgoats/goats_nft/blob/main/img/community.png). -->
1. Ability to propose and vote for DAO decisions
2. Ability to get incentives through value provided to the DAO
3. Reduction of space between true and longterm film3 builders

## DAO ORGANIZATION
<!-- ![UG dao Organization](https://github.com/Undiscoveredgoats/goats_nft/blob/main/img/ug%20dao%20organization.png). -->
<p align = "center"> <img src = "https://github.com/Undiscoveredgoats/goats_nft/blob/main/img/ug%20dao%20organization.png" width = "700" height = "250"/> </p>

The DAO at its ideal frame work is divided into five parts, the sustainable success of the DAO will
depend on the values from this HERDS:
1. **DEVs HERD**
* This herd is where all technically goats meet, talk and build together different tools for the DAO. This
herd is responsible for executing any technical goals of the community, creating tools and unique tech
solutions to provide substanial technological value to the goats.

2. **ARTISITC HERD**
* This herd is where all digital artist, filmmakers and artist of all kinds meet, showcase they're art, network
with those looking to acquire creatives for there upcoming project. Responsible for reviewing content
creative content that is used for the DAO.

3. **MEDIA HERD**
* This herd is responsible for producing daily reports on all of the happenings in DAO and the NFT/
Crypto space. Media herd keeps citizens interlinked while highlighting the innovative and exciting
projects being built by the DAO.

4. **OUTREACH HERD**
* Outreach represents the DAOs goats in discussions with external projects to bridge communities &
extend value to other departments within the DAO. We establish, foster, and cultivate relationships with
external founders and teams

5. **RESEARCH HERD**
* Here, a robust group of goats dig in, review, challenge, advise on a large number of things. From
supporting our internal Herds such as Outreach and Heardquaters, to helping goats led projects with
advice and review... and everything in between

6. **HEADQUARTERS**
* Headquarters is an investment platform for seed-stage web3 projects formed by and for community members. This is responsible for oversee day to day activities of the DAO and make sure
they align with the values of the DAO

# TECHNICAL PART
# Goat Nft Project
This project descibes the functionalities of the Goat NFT project, including minting, setting the token URL, storing images to Pinata (IPFS), and running tests. It comes with the NFT Contract, a contract test, and a script that deploys and interacts with the contract. The project is tested on local development network and the BSC testnet.

## Getting Started
### Requirements
* Pip and pipx
* Brownie
* 

### QuickStart
To clone the repo, run the following command in your shell:

```bash
git clone https://github.com/Undiscoveredgoats/goat_nft.git
```

To install dependencies and packages, run either of the following commands:

```
yarn install
```

or

```
npm install
```
Make sure you have an eth account whih has link and tBNB on Bsc-test network. Set the `PRIVATE_KEY` in `.env` as shown in `.envexample`.
To be able to upload images to Pinata, set the `PINATA_API_SECRET` and `PINATA_API_KEY` variables on scripts/UPLOAD_TO_PINATA.py as obtained from [Pinata](https://app.pinata.cloud/pinmanager#) by logging in and generating new keys. Also create and fund chainlink vrf subscription on bsc testnet [here](https://vrf.chain.link/chapel/) to be able to use chainlink randomness on goat contract.
You can also customize the goat mint fees on brownie-config.yaml

### Compiling contracts

To compile the contracts, run the following command:

```
brownie run scripts/deploy_goat.py
```


### Deploying Goat

To deploy `fuchaContract` on the Hardhat dev network, run the following command:

```
brownie run scripts/deploy_goat.py
```
This script will deploy goat, add goat to consumer, mint a randomn nft, create metadata, upload both the image and metadata to both Ipfs and Pinata, set the token metadata uri on the minted goat Id, and finally withdraw half of the goat's balance to your account.

#### Deploying on Bsc testnet
To deploy `goat` to the bsc testnet, run the followinng command:

```
brownie run scripts/deploy_goat --network bsc-test
```
This script will deploy goat, add goat to consumer, mint a randomn nft, create metadata, upload both the image and metadata to both Ipfs and Pinata, set the token metadata uri on the minted goat Id, and finally withdraw half of the goat's balance to your account.


### Testing

To run tests, enter the following command:

```
brownie test
```



