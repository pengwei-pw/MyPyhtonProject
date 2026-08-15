import pyaudio

# 初始化PyAudio
p = pyaudio.PyAudio()

# 获取设备数量
device_count = p.get_device_count()

# 遍历所有设备并打印输出设备名称
for i in range(device_count):
    device_info = p.get_device_info_by_index(i)
    if device_info["maxOutputChannels"] > 0:  # 检查设备是否是输出设备
        print(f"输出设备名称: {device_info['name']}")
        
# 关闭PyAudio
p.terminate()
