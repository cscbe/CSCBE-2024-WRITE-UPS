from pwn import *
from tqdm import tqdm


def solve(hostname, port):
    conn = remote(hostname, port)

    for bunny_index in tqdm(range(1, 1001)):
        found = False
        current_box = bunny_index
        while not found:
            conn.recvuntil(b">>>", timeout=15).decode()
            box_index = str(current_box).strip()
            conn.sendline(box_index.encode())
            result = conn.recvline().decode()
            content = result.split(" ")[-1]
            found = int(content.strip()) == bunny_index
            current_box = content
    flag = conn.recvall().decode().splitlines()[-1]
    print(flag)


if __name__ == "__main__":
    h, p = sys.argv[1], sys.argv[2]
    solve(h, p)
