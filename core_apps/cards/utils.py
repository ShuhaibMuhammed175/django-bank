import hashlib
import hmac
import random
from os import getenv

BANK_CARD_PREFIX = getenv("BANK_CARD_PREFIX")
BANK_CARD_CODE = getenv("BANK_CARD_CODE")


def generate_card_number(
    prefix=BANK_CARD_PREFIX, card_code=BANK_CARD_CODE, length=16
) -> str:
    total_prefix = prefix + card_code
    random_digits_length = length - len(total_prefix) - 1

    if random_digits_length < 0:
        raise ValueError(f"Prefix and code are too long for the specified card length")

    number = total_prefix

    number += "".join([str(random.randint(0, 9)) for _ in range(random_digits_length)])

    digits = [int(d) for d in number]

    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    check_digit = (10 - sum(digits) % 10) % 10

    return number + str(check_digit)

"""
HMAC (Hash-based Message Authentication Code)

HMAC is a security mechanism used to:
- Verify data integrity (data was not changed)
- Verify authenticity (data truly came from the sender)

How it works:
HMAC = Hash(message + secret key)

Example:
Message → "Hello"
Secret key → "mysecret123"
Output → a cryptographic hash (example: 7f4d2c1aa8e...)

Imagine you want to send a message:
Hello
You and your friend both share a secret key like:
mysecret123
HMAC combines:
message + secret key → cryptographic hash
Example HMAC result:
7f4d2c1aa8e...

Why it is useful:
If someone changes the message, the hash will no longer match.
Only someone who has the secret key can generate the correct HMAC.

Where it is used:
- API authentication (AWS, Stripe, Razorpay)
- JWT HS256 signing
- Webhooks
- Securing communication

Python Example:
----------------
import hmac, hashlib

message = b"hello"
secret = b"mysecret"

hash_value = hmac.new(secret, message, hashlib.sha256).hexdigest()
print(hash_value)

"""
def generate_cvv(card_number, expiry_date):
    secret_key = getenv("CVV_SECRET_KEY").encode()

    data = f"{card_number}{expiry_date}".encode()

    hmac_obj = hmac.new(secret_key, data, hashlib.sha256)

    cvv = str(int(hmac_obj.hexdigest(), 16))[:3]
    #zfill is zerofill add zeros to get desired length
    return cvv.zfill(3)