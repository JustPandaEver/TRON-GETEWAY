from typing import Optional, List

from pydantic import BaseModel, Field
from hdwallet.utils import generate_mnemonic


class BodyCreateWallet(BaseModel):
    mnemonicPhrase: Optional[str] = Field(description="Mnemonic Phrase", default=None)

    index: Optional[List[int]] = Field(
        description="Account and Address number. Only if mnemonicPhrase is available.", default=[0, 0]
    )

    def __init__(self, **kwargs):
        super(BodyCreateWallet, self).__init__(**kwargs)
        if self.mnemonicPhrase is None or self.mnemonicPhrase == "string":
            self.mnemonicPhrase = generate_mnemonic(language="english", strength=128)


class ResponseCreateWallet(BaseModel):
    mnemonicPhrase: str = Field(description="Mnemonic Phrase")
    privateKey: str = Field(description="Private key from the wallet")
    publicKey: str = Field(description="Public key from the wallet")
    address: str = Field(description="Wallet address")

    index: Optional[List[int]] = Field(
        description="Account and Address number. Only if mnemonicPhrase is available.", default=[0, 0]
    )

    def __init__(self, **kwargs):
        super(ResponseCreateWallet, self).__init__(**kwargs)
        if self.index is None or self.index == [0, 0]:
            del self.index
