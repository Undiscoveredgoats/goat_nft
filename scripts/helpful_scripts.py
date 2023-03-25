from brownie import accounts, network, VRFCoordinatorV2Mock, config
import eth_utils
from pathlib import Path
import requests

LOCAL_DEVELOPMENT_NETWORKS = ["development", "local-ganache"]
FORKED_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/bsc-test/{}/{}"


def get_account():
    if (
        network.show_active() in LOCAL_DEVELOPMENT_NETWORKS
        or network.show_active() in FORKED_ENVIRONMENTS
    ):
        account = accounts[0]
    else:
        account = accounts.load("rastas")
    return account


def deploy_mocks():
    account = get_account()
    vrf_mock = VRFCoordinatorV2Mock.deploy(
        config["networks"][network.show_active()]["fee"], 250000, {"from": account}
    )
    return vrf_mock


def encode_data(initializer=None, *args):
    if len(args) == 0 or initializer == None:
        return eth_utils.to_bytes(hexstr="0x")
    else:
        return initializer.encode_input(*args)


def upgrade(account, proxy, newImplementation, proxy_admin=None, initializer=None):
    if proxy_admin:
        if initializer:
            tx = proxy_admin.upgradeAndCall(
                proxy, newImplementation, initializer, {"from": account}
            )
        else:
            tx = proxy_admin.upgrade(proxy, newImplementation, {"from": account})
    else:
        if initializer:
            tx = proxy.upgradeToAndCall(
                newImplementation, initializer, {"from": account}
            )
        else:
            tx = proxy.upgradeTo(newImplementation, {"from": account})
    return tx


def upload_to_ipfs(file_path):
    ##opening that file path passed as binary
    with Path(file_path).open("rb") as fp:
        image_file = fp.read()
        end_point = "/api/v0/add"
        ##ipfs_node obtained by running ipfs daemon to start your node
        ipfs_node = "http://127.0.0.1:5001"
        ##posting the image file to ipfs
        response = requests.post(ipfs_node + end_point, files={"file": image_file})
        ##grabbing the hash from the ipfs response.
        ipfs_hash = response.json()["Hash"]
        ##renaming ./metadata/goerli/0-pug.json to 0-pug.json
        image_file_name = file_path.split("/")[-1:][0]
        ##getting the image uri
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={image_file_name}"
        print(image_uri)
        return image_uri
