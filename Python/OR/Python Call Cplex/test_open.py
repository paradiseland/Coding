"""
do a test of open file
"""
with open('input.txt', 'r') as f:
    CONTENT = f.read()
print(CONTENT)
