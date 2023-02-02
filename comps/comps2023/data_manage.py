import json
from PIL import Image
from pyzbar import pyzbar

def parse_qr_code(fp):
    decoded:list = pyzbar.decode(Image.open(fp))
    return json.loads(decoded[0].data.decode("ascii"))

if __name__ == "__main__":
    print(parse_qr_code(r"C:\Users\tickl\Downloads\download.png"))