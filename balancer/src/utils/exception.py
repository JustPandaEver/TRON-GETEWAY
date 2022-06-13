class NotFeeResend(BaseException):
    """Error when sending native for commission"""
    pass


class NotSendToMainWallet(BaseException):
    """Error when sending the token to the main wallet"""
    pass


class NotPrivateKey(BaseException):
    """Error in obtaining a private key from the wallet"""
    pass
