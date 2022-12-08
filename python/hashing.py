class HashedString:

    M = int(1e9) + 9
    P = 9973

    def __init__(self, s: str):
        self.pow = [1]
        self.p_hash = [0]

        while len(self.pow) <= len(s):
            self.pow.append((self.pow[-1] * self.P) % self.M)

        for i in range(len(s)):
            self.p_hash.append(
                ((self.p_hash[i] * self.P) + ord(s[i])) % self.M)

    def get_hash(self, start, end):
        raw_val = (
            self.p_hash[end] -
            (self.p_hash[start] * self.pow[end - start])
        )
        # return (raw_val % self.M + self.M) % self.M
        return raw_val % self.M


string = 'ABCABCDE'
h = HashedString(string)
assert h.get_hash(3, 6) == HashedString("ABC").get_hash(
    0, 3) == HashedString("  ABC  ").get_hash(2, 5)

a = ['ABCABCDE', "ABC", "  ABC  "]
assert a[0][3:6] == a[1][0:3] == a[2][2:5]

print(HashedString("ABCDEFG").p_hash)
print(HashedString("ABCDEFG").pow)
