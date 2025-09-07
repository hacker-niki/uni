n = int(input())
input()

common_songs = set(input().split())

for _ in range(n - 1):
    input()
    common_songs.intersection_update(set(input().split()))

print(len(common_songs))
print(*sorted(list(common_songs)))