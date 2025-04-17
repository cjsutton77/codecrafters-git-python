import sys
import os
import zlib
import hashlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif (sys.argv[1] == "cat-file" and sys.argv[2] == "-p"):
        blobHash = sys.argv[3]
        with open(f".git/objects/{blobHash[:2]}/{blobHash[2:]}", "rb") as f:
            # Read and decompress the data from the file using zlib
            raw = zlib.decompress(f.read())
            # Split the decompressed data into a header and content at the first null byte
            header, content = raw.split(b"\0", maxsplit=1)
            # Print the content part, decoding it from bytes to a UTF-8 string
            print(content.decode(), end="")
    elif (sys.argv[1] == "hash-object" and sys.argv[2] == "-w"):
        with open(f"{sys.argv[3]}", "rb") as f:
            obj = f.read()
            # Add header
            result = b'blob ' + str(len(obj)).encode() + b'\x00' + obj
            # # Compute hash
            sha = hashlib.sha1(result).hexdigest()
            # Write hash
            print(sha)
            os.mkdir(f".git/objects/{sha[:2]}")
            with open(f".git/objects/{sha[:2]}/{sha[2:]}", "wb") as fd:
                fd.write(zlib.compress(result))
    else:
        raise RuntimeError(f"Unknown command #{command}")

if __name__ == "__main__":
    main()
