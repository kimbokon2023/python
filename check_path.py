import sys
print("파이썬 실행 위치:", sys.executable)
print("\n[현재 sys.path]")
for path in sys.path:
    print(" -", path)
