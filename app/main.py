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
            sha = hashlib.sha1(result).hexdigest()
            # Write hash
            print(sha)
            os.mkdir(f".git/objects/{sha[:2]}")
            with open(f".git/objects/{sha[:2]}/{sha[2:]}", "wb") as fd:
                fd.write(zlib.compress(result))
    elif (sys.argv[1] == "ls-tree" and sys.argv[2] == "--name-only"):
        treeHash = sys.argv[3]
        with open(f".git/objects/{treeHash[:2]}/{treeHash[2:]}", "rb") as f:
            # Read the compressed data from the file and decompress it using zlib
            raw = zlib.decompress(f.read())
            
            # Split the decompressed data into a header and content at the first null byte
            header, content = raw.split(b'\x00', 1)
            
            # Iterate through the content to parse each entry in the tree
            while content:
                # Split the content into the current entry's header and the remaining content
                header, content = content.split(b'\x00', maxsplit=1)
                
                # This skips the first 20 bytes of the current entry 
                # in the tree, which is the SHA-1 hash of the object 
                # being referenced. The remaining data is processed 
                # to extract the next entry.
                content = content[20:]
                
                # Decode the header (mode and name) into a UTF-8 string and split it into components
                out = header.decode('utf-8').split(' ')
                
                # Print the name of the file or directory (second part of the split)
                print(out[1], end='\n')
    else:
        raise RuntimeError(f"Unknown command #{command}")

if __name__ == "__main__":
    main()

