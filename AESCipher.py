import base64
from typing import Union

from Cryptodome.Cipher import AES


class AESCipher:

    def __init__(self, key: str, iv: str = "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0") -> None:
        self.key = key[0:16].encode('utf-8')  # 只截取16位
        self.iv = iv.encode('utf-8')  # 16位字符，用来填充缺失内容，可固定值也可随机字符串，具体选择看需求。

    def __pad(self, text: str) -> str:
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text: str) -> str:
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, raw: str) -> bytes:
        """加密"""
        raw = self.__pad(raw).encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc: Union[str, bytes]) -> str:
        """解密"""
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.__unpad(cipher.decrypt(enc).decode("utf-8"))


def __test() -> None:
    e = AESCipher('dacf107e4bdbbef0', 'bcancid682e09aec')
    secret_data = "19184236244"
    enc_str = e.encrypt(secret_data)
    print('enc_str: ' + enc_str.decode())
    dec_str = e.decrypt(enc_str)
    print('dec str: ' + dec_str)


if __name__ == '__main__':
    raise SystemExit(__test())
