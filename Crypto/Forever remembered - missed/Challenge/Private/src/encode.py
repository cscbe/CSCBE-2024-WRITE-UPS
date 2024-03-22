import base64
def encode(flag):
    b64 = str(base64.b64encode(flag.encode()))[2:-1]
    res = "".join(str(int(str(format(ord(i),'08b')))+11111111) for i in b64)
    return res

def main():
    with open("flag.txt","r") as f:
        print(encode(f.read()))

if __name__=="__main__":
    main()