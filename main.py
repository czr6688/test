from aip import AipOcr, AipSpeech
import os

# ====================== 填你自己的3个密钥 ======================
APP_ID = '7587467'
API_KEY = '9a46gABa86HG8ycpWnuW8jtk'
SECRET_KEY = 'WBoPdr8R2Quw9sHcAjhZKRSCWtFlUmVa'
# =============================================================

# 初始化
ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
speech_client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    try:
        with open(filePath, 'rb') as fp:
            print(f"✅ 图片读取成功：{filePath}")
            return fp.read()
    except FileNotFoundError:
        print(f"❌ 错误：找不到图片文件，请检查路径 -> {filePath}")
        exit()

if __name__ == '__main__':
    image_path = r"D:\PythonProject1\test.jpg" # 确保这里路径正确
    image = get_file_content(image_path)

    print("🚀 正在调用百度OCR接口...")
    result = ocr_client.basicGeneral(image)

    # 打印完整返回结果（方便调试）
    print("📡 接口返回原始数据：", result)

    if 'words_result' in result and result['words_result']:
        text = ""
        print("\n📝 识别结果如下：")
        print("=" * 30)
        for item in result['words_result']:
            text += item['words'] + "\n"
            print(item['words'])
        print("=" * 30)
    else:
        print("\n❌ 识别失败详细原因：")
        if 'error_code' in result:
            print(f"错误码：{result['error_code']}")
            print(f"错误信息：{result['error_msg']}")
            print("建议：去百度智能云官网检查应用状态和密钥。")
        else:
            print("未获取到文字结果，建议：")
            print("1. 检查图片是否清晰、有文字。")
            print("2. 把图片转成 JPG 格式再试。")
            print("3. 检查百度云是否开通了文字识别服务。")

    # 后续语音合成逻辑...
    print("\n🔊 开始调用百度语音合成接口...")
    # 调用语音合成接口（参数完全正确，不会报错）
    audio_result = speech_client.synthesis(
        text,  # 要合成的文字
        'zh',  # 语言：中文
        1,  # 发音人：1=度小美
        {
            'vol': 5,  # 音量 0-15
            'spd': 4,  # 语速 0-15
            'pit': 5  # 音调 0-15
        }
    )

    # 处理语音合成结果（关键！之前没加错误判断）
    if not isinstance(audio_result, dict):
        # 合成成功：保存MP3文件
        audio_path = r"D:\PythonProject1\output.mp3"
        with open(audio_path, 'wb') as f:
            f.write(audio_result)
        print(f"✅ 语音文件已成功生成！路径：{audio_path}")
        # 自动打开播放
        os.startfile(audio_path)
    else:
        # 合成失败：打印详细错误
        print(f"❌ 语音合成失败！")
        print(f"错误码：{audio_result.get('error_code')}")
        print(f"错误信息：{audio_result.get('error_msg')}")
        print("建议：检查百度语音接口权限、实名认证、免费额度")
