from web3 import Web3
import requests
import time
import random
import json as js


time_delay_min = 30  # Минимальная и
time_delay_max = 60  # Максимальная задержка между акками в секундах

RETRY = 20


def check_transaction_receipt(web3, _hash):
    try:
        web3.eth.get_transaction_receipt(_hash)
        print('Транзакция смайнилась успешно')
        return 0
    except Exception as error:
        print(f'Транзакция еще не смайнилась  ||  {error}')
        return 1


def get_transaction_receipt(web3, _hash):
    try:
        time.sleep(5)
        txn_receipt = web3.eth.get_transaction_receipt(_hash)
        return str(txn_receipt['status'])
    except:
        return 0


def mint(private_key, retry=0):
    try:
        web3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/bsc'))
        address_wallet = web3.eth.account.from_key(private_key).address
        print(f'Сейчас работает аккаунт - {address_wallet}\n')
        addres_contract = Web3.to_checksum_address('0x2c980cc4a626e46c8940267b9ea17051f1db68ed')
        abi = '[{"inputs":[{"internalType":"address","name":"_signer","type":"address"},{"internalType":"uint256","name":"_startTime","type":"uint256"},{"internalType":"uint256","name":"_endTime","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"nftID","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_dummyId","type":"uint256"},{"indexed":false,"internalType":"address","name":"_nft","type":"address"},{"indexed":false,"internalType":"address","name":"_mintTo","type":"address"}],"name":"EventClaim","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"signer","type":"address"}],"name":"eveUpdateSigner","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"startTime","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"endTime","type":"uint256"}],"name":"eveUpdateTime","type":"event"},{"inputs":[{"internalType":"address","name":"_nft","type":"address"},{"internalType":"uint256","name":"_dummyId","type":"uint256"},{"internalType":"address","name":"_mintTo","type":"address"},{"internalType":"bytes","name":"_signature","type":"bytes"}],"name":"claim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_signer","type":"address"},{"internalType":"uint256","name":"_startTime","type":"uint256"},{"internalType":"uint256","name":"_endTime","type":"uint256"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"isClaimed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numClaimed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_signer","type":"address"}],"name":"setSigner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"signer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startTime","type":"uint256"},{"internalType":"uint256","name":"_endTime","type":"uint256"}],"name":"updateTime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_nft","type":"address"},{"internalType":"uint256","name":"_dummyId","type":"uint256"},{"internalType":"address","name":"_mintTo","type":"address"},{"internalType":"bytes","name":"_signature","type":"bytes"}],"name":"userCanClaim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userClaimed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'
        contract = web3.eth.contract(address=addres_contract, abi=abi)

        url = 'https://combonetwork.io/api/twitter/bind'
        json = {
            'address': address_wallet
        }

        requests.post(url=url, json=json)
        time.sleep(2)
        url = 'https://combonetwork.io/api/telegram/join'
        requests.post(url=url, json=json)
        time.sleep(2)

        url = 'https://combonetwork.io/api/mint/sign'
        json = {
            'chain_id': 56,
            'mint_contract': "0x2C980cc4A626e46c8940267b9eA17051f1DB68Ed",
            'mint_to': address_wallet,
            'nft_contract': "0x9e8C1e7B35f646A606644a5532C6103C647938cf"
        }

        res = requests.post(url=url, json=json)
        data = res.json()
        signature = data['data']['signature']
        dummy_id = int(data['data']['dummy_id'])

        dick = {
            'from': address_wallet,
            'nonce': web3.eth.get_transaction_count(address_wallet),
            'gasPrice': Web3.to_wei(1, 'gwei')
        }
        nft_contract = Web3.to_checksum_address('0x9e8C1e7B35f646A606644a5532C6103C647938cf')
        tx = contract.functions.claim(nft_contract, dummy_id, address_wallet, signature).build_transaction(dick)
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        raw_tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = web3.to_hex(raw_tx_hash)
        count = 0
        while check_transaction_receipt(web3, tx_hash):
            count += 1
            if count > RETRY:
                print('Транзакция сфейлилась, пытаюсь еще раз')
                return 0
            time.sleep(30)
        while True:
            res_ = get_transaction_receipt(web3, tx_hash)
            if res_ == '0':
                print('Транзакция сфейлилась, пытаюсь еще раз')
                return 0
            elif res_ == '1':
                break
            elif res_ == 0:
                continue

        print(f'mint || https://bscscan.com/tx/{tx_hash}\n')
        return 1

    except Exception as error:
        print(error)
        retry += 1
        if retry > 10:
            return 0
        mint(private_key, retry)


if __name__ == '__main__':
    print('  _  __         _               _                                           _ _         ')
    print(' | |/ /___   __| | ___ _ __ ___| | ____ _ _   _  __ _        _____   ____ _| | | ____ _ ')
    print(r" | ' // _ \ / _` |/ _ \ '__/ __| |/ / _` | | | |/ _` |      / __\ \ / / _` | | |/ / _` |")
    print(r' | . \ (_) | (_| |  __/ |  \__ \   < (_| | |_| | (_| |      \__ \\ V / (_| | |   < (_| |')
    print(r' |_|\_\___/ \__,_|\___|_|  |___/_|\_\__,_|\__, |\__,_|      |___/ \_/ \__,_|_|_|\_\__,_|')
    print('                                          |___/                                    ', '\n')
    print('https://t.me/developercode1')
    print('https://t.me/developercode1')
    print('https://t.me/developercode1\n')

    with open("private_key.txt", "r") as f:
        keys_list = [row.strip() for row in f]

    random.shuffle(keys_list)

    while keys_list:
        key = keys_list.pop(0)
        mint(key)
        time.sleep(random.randint(time_delay_min, time_delay_max))
