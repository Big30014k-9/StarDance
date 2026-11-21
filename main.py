import hashlib, math, struct
from pathlib import Path
from PIL import Image


MAGIC = b"WSTR"

def pack(path):
    data = path.read_bytes()
    name = path.name.encode()
    header = MAGIC + struct.pack(">BI", len(name), len(data)) + name
    return header + data


def unpack(blob):
    if blob[:4] != MAGIC:
        raise ValueError("this isn't one of ours!")
    name_len, data_len = struct.unpack(">BI", blob[4:9])
    name = blob[9:9 + name_len].decode()
    data = blob[9 + name_len:9 + name_len + data_len]
    if len(data) != data_len:
        raise ValueError("the file got cut off")
    return name, data



def encode(blob, out):
    side = math.ceil(math.sqrt(len(blob) / 3))
    blob += bytes(side * side * 3 - len(blob))
    Image.frombytes("RGB", (side, side), blob).save(out)

def decode(path):
    return Image.open(path).convert("RGB").tobytes()



def main():
    resposta = input("Deseja codificar ou decodificar? (c/d): ").strip().lower()
    if resposta == "c":
        imagem = input("Digite o caminho da imagem a ser codificada: ").strip()
        nome_arquivo = input("Digite o nome do arquivo de saída (com extensão .png): ").strip()
        encode(pack(Path(imagem)), nome_arquivo)


    elif resposta == "d":
        imagem = input("Digite o caminho da imagem a ser decodificada: ").strip()
        nome_arquivo = input("Digite o nome do arquivo de saída (com extensão .jpg): ").strip()
        name, data = unpack(decode(imagem))
        Path("recovered").mkdir(exist_ok=True)
        Path("recovered", Path(name).name).write_bytes(data)
        print(hashlib.sha256(Path(imagem).read_bytes()).hexdigest())
        print(hashlib.sha256(data).hexdigest())


main()