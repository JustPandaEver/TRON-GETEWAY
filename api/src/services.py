import typing

from hdwallet import BIP44HDWallet
from hdwallet.derivations import BIP44Derivation
from hdwallet.cryptocurrencies import TronMainnet

from src.schemas import BodyCreateWallet, ResponseCreateWallet


class Service:
    @staticmethod
    async def create_new_wallet(body: BodyCreateWallet) -> ResponseCreateWallet:
        """Create tron wallet"""
        hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=TronMainnet)
        hdwallet.from_mnemonic(mnemonic=body.mnemonicPhrase, language="english")
        return ResponseCreateWallet(
            mnemonicPhrase=body.mnemonicPhrase,
            privateKey=hdwallet.private_key(),
            publicKey=hdwallet.public_key(),
            address=hdwallet.address()
        )

    @staticmethod
    async def generate_wallet(body: BodyCreateWallet) -> ResponseCreateWallet:
        """Generate account if have mnemonic phrase"""
        hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=TronMainnet)
        hdwallet.from_mnemonic(mnemonic=body.mnemonicPhrase, language="english")
        derivation = BIP44Derivation(
            cryptocurrency=TronMainnet, account=body.index[0], change=False, address=body.index[1]
        )
        hdwallet.from_path(path=derivation)
        return ResponseCreateWallet(
            mnemonicPhrase=body.mnemonicPhrase,
            privateKey=hdwallet.private_key(),
            publicKey=hdwallet.public_key(),
            address=hdwallet.address(),
            index=body.index
        )


service = Service
