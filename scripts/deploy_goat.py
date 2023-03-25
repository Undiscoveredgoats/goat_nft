from scripts.helpful_scripts import (
    get_account,
    encode_data,
    LOCAL_DEVELOPMENT_NETWORKS,
    deploy_mocks,
    upload_to_ipfs,
    OPENSEA_URL,
)
from brownie import goats_nft, config, network, interface, Contract

from metadata.sample_metadata import sample_metadata_template
import time
from pathlib import Path
import os
import json

from scripts.upload_to_pinata import upload_to_pinata

funding_amount = 10000000000000000000
randomWords = [7667, 89789]

breed_to_image_uri = {
    "goat": "https://ipfs.io/ipfs/QmVoqA3SyKUvRSQmvGGWRvM583TtE33wzXJa3xbutLCAVt?filename=goat.jpg",
    "grind": "",
    "jump": "",
    "kompyuta": "",
    "mbuzi_head": "",
}


breed_to_metadata_uri = {
    "goat": "https://ipfs.io/ipfs/QmaE3WtLe9P23zDVnYxVMbX4oG6VYKJToQCQ2oJFsVF75t?filename=0-goat.json",
    "grind": "",
    "jump": "",
    "kompyuta": "",
    "mbuzi_head": "",
}


def deploy_goat():
    account = get_account()
    # checking for mocks
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        vrf = deploy_mocks()
        vrf_address = vrf.address
    else:
        vrf_address = config["networks"][network.show_active()]["VRFCoordinator"]
        vrf = interface.VRFCoordinatorV2Interface(vrf_address)

    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        vrf_tx = vrf.createSubscription({"from": account})
        sid = vrf_tx.events["SubscriptionCreated"]["subId"]
        print("Yeay created subscription")
        # adding goat as consumer
    else:
        sid = config["networks"][network.show_active()]["sId"]
    print(f"The sID is {sid}")
    # deploying goat

    goat = goats_nft.deploy(
        "Goat",
        "UGT",
        vrf_address,
        config["networks"][network.show_active()]["keyHash"],
        sid,
        config["networks"][network.show_active()]["mintFee"],
        {"from": account},
    )
    print(f"Yeay deployed goat to address:{goat.address}")

    # getting the sid,adding consumer and funding subscription
    # adding consumers
    # add_tx = vrf.addConsumer(sid, goat.address, {"from": account})
    # add_tx.wait(1)
    # balance, req_count, owner, consumers = vrf.getSubscription(sid, {"from": account})
    # print(balance, req_count, owner, consumers)
    return goat, vrf, account, sid


def addConsumer(vrf, sid, goat, account):
    add_tx = vrf.addConsumer(sid, goat.address, {"from": account})
    add_tx.wait(1)
    print("Yeay added goat as consumer")
    # funding the subscription
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        fund_tx = vrf.fundSubscription(sid, funding_amount, {"from": account})
        fund_tx.wait(1)
        print("Yeay funded the subscription with 10 link")


def mintNft(account, goat, vrf, sid):

    # minting nft
    create_tx = goat.createGoat(
        {"from": account, "value": config["networks"][network.show_active()]["mintFee"]}
    )
    create_tx.wait(1)
    request_id = create_tx.events["requestedNft"]["requestId"]
    print(f"THE requestId is {request_id}")
    if network.show_active() in LOCAL_DEVELOPMENT_NETWORKS:
        vrf.fulfillRandomWordsWithOverride(
            request_id, goat, randomWords, {"from": account}
        )
        # vrf.fulfillRandomWords(request_id, goat, {"from": account})
        tokenId = goat.tokenCounter() - 1
        print(tokenId)
        print(f"Yeay minted goat of breed: {goat.TokenIdToBreed(tokenId)}")
    else:
        time.sleep(120)
        tokenId = goat.tokenCounter()
        print(f"Yeay minted goat of breed: {goat.TokenIdToBreed(tokenId)}")


def creata_metadata(goat, image_uri=None):
    no_of_collectibles = goat.tokenCounter()
    ##looping through all created collectibles
    for tokenId in range(no_of_collectibles):
        ##getting the breed
        breed = goat.TokenIdToBreed(tokenId)
        ## shiba - inu = shiba-inu(breed_file)
        # breed_file = breed.replace(" ", "")
        ##'./metadata/goerli/0-pug.json'
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{tokenId}-{breed}.json"
        )
        ##checking whether the medata_file name exists
        if Path(metadata_file_name).exists() == True:
            print(
                f"{metadata_file_name} file exists, delete the current one to override it!!"
            )
        else:
            print(f"Creating {metadata_file_name} file...")
            ##setting the breed_metadata to the template dictionary and overrting it with the breed info
            breed_metadata = sample_metadata_template
            breed_metadata["name"] = breed
            breed_metadata["description"] = f"Greatest {breed} of all time!"
            image_file_path = "./img/" + f"{breed}" + ".jpg"  ##'./img/pug.png'
            print(image_file_path)
            image_uri = upload_to_ipfs(image_file_path)
            upload_to_pinata(image_file_path)
            # ##checking whether its allowed to upload to ipfs from the env variable so that it does not always upload to ipfs when this script is run
            # if os.getenv("UPLOAD_TO_IPFS") == "true":
            #     image_uri = upload_to_ipfs(image_file_path)
            #     ##upload_to_pinata(image_file_path)
            # else:
            #     if image_uri:
            #         image_uri = image_uri
            #     else:
            #         image_uri = breed_to_image_uri[breed]
            print(image_uri)
            breed_metadata["image"] = image_uri
            print(breed_metadata)
            ##saving the breed_metadata dict to the metadata file name in json format
            with open(metadata_file_name, "w") as file:
                json.dump(breed_metadata, file)
                file.close()
                metadata_uri = upload_to_ipfs(metadata_file_name)
                upload_to_pinata(metadata_file_name)
                # if os.getenv("UPLOAD_TO_IPFS") == "true":
                #     upload_to_ipfs(metadata_file_name)
                # else:
                #     metadata_uri = breed_to_metadata_uri[breed]
                print(f"the metadata uri of the {breed} is {metadata_uri}")


def withdraw(goat, amount, owner):
    initial_balance = goat.balance()
    print(f"The initial balance of goat is {initial_balance}")
    withdraw_tx = goat.withdraw(amount, {"from": owner})
    withdraw_tx.wait(1)
    final_balance = goat.balance()
    print(f"The final balance of goat is {final_balance}")


def setTokenUri(goat):
    no_of_collectibles = goat.tokenCounter()
    ##looping through all nft tokens created
    for tokenId in range(no_of_collectibles):
        breed = goat.TokenIdToBreed(tokenId)
        # breed_file = breed.replace(" ", "")
        metadata_uri = breed_to_image_uri[breed]
        ##checking if the token uri of the selected breed exists
        if not goat.tokenURI(tokenId).startswith("https://"):
            set_tokenUri(tokenId, goat, metadata_uri)
            read_data(tokenId, goat)
        else:
            print(f"the token URI of {tokenId}-{breed} is {goat.tokenURI(tokenId)}")
        # print(
        #     f"Now You can view your nft on {OPENSEA_URL.format(goat.address, tokenId)}"
        # )


def set_tokenUri(tokenId, tokenContract, tokenUri):
    account = get_account()
    tokenContract.setTokenUri(tokenId, tokenUri, {"from": account})


def read_data(tokenId, goat):
    print(
        f"The token uri of {tokenId}-{goat.TokenIdToBreed(tokenId)} is {goat.tokenURI(tokenId)}"
    )


def main():
    goat, vrf, account, sid = deploy_goat()
    # account = get_account()
    # vrf_address = config["networks"][network.show_active()]["VRFCoordinator"]
    # goat = Contract.from_abi(
    #     "Goat", "0xf0503fcFF64ed7B6a038c9D38baA47E5e00dF05e", goats_nft.abi
    # )
    # vrf = interface.VRFCoordinatorV2Interface(vrf_address)
    # sid = config["networks"][network.show_active()]["sId"]
    addConsumer(vrf, sid, goat, account)
    amount = config["networks"][network.show_active()]["mintFee"]
    withdraw_amount = amount / 2
    # account = get_account()
    # vrf_address = config["networks"][network.show_active()]["VRFCoordinator"]
    # goat = goats_nft("0x25FEA8Ef161bEef0Ba537e33B0b98CFbEAb05D66")
    # vrf = interface.VRFCoordinatorV2Interface(vrf_address)
    mintNft(account, goat, vrf, sid)
    creata_metadata(goat)
    setTokenUri(goat)
    withdraw(goat, withdraw_amount, account)
