# ❌ Buggy logic – infinite loop
# i = 1
# while i < 5:
#     print(i)

# ❌ i was never incremented

# ✅ Corrected loop
i = 1
while i < 5:
    print(i)
    i += 1   # Fix added
