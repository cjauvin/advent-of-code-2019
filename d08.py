from collections import Counter


s = open("d08_input.txt").read().strip()
n = 25 * 6

min_zeros = (float("inf"), -1)
for i in range(0, len(s), n):
    cnt = Counter(s[i : i + n])
    min_zeros = min(min_zeros, (cnt["0"], cnt["1"] * cnt["2"]))

print("Part 1:", min_zeros[1])

# s = "0222112222120000"
# n = 4

layers = []
for i in range(0, len(s), n):
    layers.append(s[i : i + n])

# layers = layers[::-1]

img = [0] * n
for i in range(n):
    j = 0
    while layers[j][i] == "2":
        j += 1
    img[i] = layers[j][i]

img = "".join(img).replace("0", " ").replace("1", "#")

print("Part 2:")
for i in range(6):
    print("".join(img[i * 25 : (i + 1) * 25]))
