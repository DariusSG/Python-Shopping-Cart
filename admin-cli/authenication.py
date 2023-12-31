import hashlib
import time
import binascii

# admintest1234


def salt():
    return "eb387a5edbaddb8851e28127671cec2694a817afc327a9c8eb6e90196c21a222"


def key():
    return 'aef50c0a1a1d6cf0a19feafbaef2f2d042651c1e4d2009bbf46e6164da1d03e207e6d7dc1823915456abfa62bb65bdaa9b64f3a399ffce58e58c84e9dc252f19c0a4b6dd9d56836281081ec9b2eab5257d91612daae66ff1ac8f5a57c3d9788e446c8e0f4ae47d7cb6d66c5d160833315740eb5ac77826b909de41f669cafc9b'


def authenicate(username, password):
    newpass = username + password
    if (binascii.hexlify(
            hashlib.pbkdf2_hmac('sha256', newpass.encode('utf-8'), salt().encode("ascii"), 100000, dklen=128)).decode(
            'ascii')) == 'aef50c0a1a1d6cf0a19feafbaef2f2d042651c1e4d2009bbf46e6164da1d03e207e6d7dc1823915456abfa62bb65bdaa9b64f3a399ffce58e58c84e9dc252f19c0a4b6dd9d56836281081ec9b2eab5257d91612daae66ff1ac8f5a57c3d9788e446c8e0f4ae47d7cb6d66c5d160833315740eb5ac77826b909de41f669cafc9b':
        return True
    else:
        print("Wrong Password, Try Again")
        time.sleep(1.5)
        return False
