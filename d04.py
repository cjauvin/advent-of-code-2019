def has_2_adj_digits(s):
    for i in range(len(s) - 1):
        if len(set(s[i : i + 2])) == 1:
            return True
    return False


def has_2_adj_digits2(s):
    for i in range(len(s) - 1):
        if len(set(s[i : i + 2])) == 1:
            d = s[i]
            if i > 0 and s[i - 1] == s[i]:
                continue
            if i < len(s) - 2 and s[i + 2] == s[i]:
                continue
            return True
    return False


n1 = 0
n2 = 0
for i in range(273025, 767253):
    s = str(i)
    if "".join(sorted(s)) == s:
        if has_2_adj_digits(s):
            n1 += 1
        if has_2_adj_digits2(s):
            n2 += 1

print(n1)
print(n2)
