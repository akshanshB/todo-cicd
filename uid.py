import uuid
import random
import string



def get_uid():

    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()[]<>")
    random.shuffle(characters)
    ids = list(str(uuid.uuid4()))
    uid_chars = characters+ids
    random.shuffle(uid_chars)
    uid_length=9
    def short_uid():
        count=len(uid_chars)-1
        c=''
        for i in range(0,uid_length):
            c+=uid_chars[random.randint(0,count)]
        return c
    return short_uid()