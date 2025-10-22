import os
from openai import OpenAI
from dotenv import load_dotenv
from tradingagents.default_config import DEFAULT_CONFIG

# 加载 .env 文件
load_dotenv()

def test_qwen_api_connection():
    print("--- Testing Qwen API Connection ---")

    # 获取配置
    qwen_api_key = os.getenv("DASHSCOPE_API_KEY")
    qwen_base_url = DEFAULT_CONFIG["backend_url"]
    qwen_model = DEFAULT_CONFIG["quick_think_llm"] # 使用一个Qwen模型进行测试

    if not qwen_api_key:
        print("错误：未找到 DASHSCOPE_API_KEY 环境变量。请确保在系统环境变量中设置了此变量。")
        return

    if not qwen_base_url:
        print("错误：default_config.py 中未配置 Qwen 的 backend_url。")
        return

    print(f"尝试连接 Qwen API，Base URL: {qwen_base_url}, Model: {qwen_model}")

    try:
        client = OpenAI(
            api_key=qwen_api_key,
            base_url=qwen_base_url,
        )

        completion = client.chat.completions.create(
            model=qwen_model,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '你好，请简单介绍一下你自己。'}
            ],
            temperature=0, # 降低随机性，使测试结果更稳定
        )

        response_content = completion.choices[0].message.content
        print("\n--- Qwen API 连接成功！---")
        print("模型响应示例：")
        print(response_content)
        print("--------------------------")

    except Exception as e:
        print("\n--- Qwen API 连接失败！---")
        print(f"错误信息：{e}")
        print("请检查以下几点：")
        print("1. 您的 DASHSCOPE_API_KEY 是否正确且有效。")
        print("2. 您的网络连接是否正常。")
        print("3. default_config.py 中的 backend_url 是否正确。")
        print("--------------------------")

if __name__ == "__main__":
    test_qwen_api_connection()
