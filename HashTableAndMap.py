class HashTableEntry:
    def __init__(self, key, item):
        self.key = key
        self.item = item

class HashMap:
    # O(n)
    def __init__(self, initial_capacity=10):
        self.map = []
        for i in range(initial_capacity):
            self.map.append([])

    def getHash(self, key):
        bucket = int(key) % len(self.map)
        return bucket

    #O(1) typically, but worst case o(n)
    def insert(self, key, value):
        key_hash = self.getHash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = key_value
                    return True
            self.map[key_hash].append(key_value)
            return True

    #avg O(1) but can be O(n) worst case
    def get(self, key):
        key_hash = self.getHash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    #O(n)
    def update(self, key, value):
        key_hash = self.getHash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    print(pair[1])
                    return True

    #O(n)
    def delete(self, key):
        key_hash = self.getHash(key)
        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True
        return False