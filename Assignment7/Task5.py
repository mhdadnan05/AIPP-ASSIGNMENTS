# ❌ Buggy Code
# nums = [1,2,3]
# print(nums[5])  # IndexError

# ✔ Safe Access Handling

nums = [1, 2, 3]

index = 5
if index < len(nums):
    print(nums[index])
else:
    print("Index out of range! Max index =", len(nums)-1)
