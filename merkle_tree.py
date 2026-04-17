import hashlib
import sys

def hash_file(filename, algorithm):
    h = hashlib.new(algorithm)
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def hash_pair(left, right, algorithm):
    h = hashlib.new(algorithm)
    h.update((left + right).encode())
    return h.hexdigest()

def build_merkle_tree(files, algorithm):
    leaf_hashes = []

    for file in files:
        leaf_hashes.append(hash_file(file, algorithm))

    print("Leaf hashes:")
    for i in range(len(files)):
        print(files[i], "->", leaf_hashes[i])

    current_level = leaf_hashes[:]

    level_num = 1
    while len(current_level) > 1:
        next_level = []
        print("\nLevel", level_num)

        i = 0
        while i < len(current_level):
            left = current_level[i]

            if i + 1 < len(current_level):
                right = current_level[i + 1]
            else:
                right = left

            parent = hash_pair(left, right, algorithm)
            next_level.append(parent)

            print("Hash(", left, ",", right, ") =", parent)
            i += 2

        current_level = next_level
        level_num += 1

    return current_level[0]

def main():
    if len(sys.argv) < 3:
        print("Usage: python merkle_tree.py sha1 file1 file2 file3 ...")
        return

    algorithm = sys.argv[1].lower()
    files = sys.argv[2:]

    if algorithm != "md5" and algorithm != "sha1":
        print("Use md5 or sha1 only")
        return

    top_hash = build_merkle_tree(files, algorithm)
    print("\nTop Hash:", top_hash)

if __name__ == "__main__":
    main()
