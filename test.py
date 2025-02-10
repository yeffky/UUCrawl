import hashlib
import time

def le(e):
    # 第一次MD5，将输入转换为字符串并计算MD5
    first_md5 = hashlib.md5(str(e).encode()).hexdigest()
    # 拼接字符串并第二次计算MD5
    combined = first_md5
    second_md5 = hashlib.md5(combined.encode()).hexdigest()
    return second_md5

# 获取当前时间的毫秒级时间戳（与JavaScript的new Date().getTime()等效）
t = int(time.time() * 1000)
# 计算最终结果
o = le(t)

print("Timestamp:", t)
print("Result:", o)