import base64


def encode_img(img_path) -> bytes:
    with open(img_path, 'rb') as avt:
        avatar_img = base64.b64encode(avt.read())
    return avatar_img
