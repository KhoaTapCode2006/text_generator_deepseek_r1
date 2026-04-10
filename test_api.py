import requests
import json
import time

API_URL = "http://127.0.0.1:8000/generate"

test_cases = [
    {
        "name": "Test case Logic/Toán học",
        "prompt": "If I have 5 oranges, I gave you 2 oranges, then I buy 3 more oranges. How many do I have? Explain shortly.",
        "max_new_tokens": 512
    },
    {
        "name": "Test case Lập trình (Python)",
        "prompt": "Write a Python code to calculate the factorial of a positive integer N.",
        "max_new_tokens": 1028
    }
]

def run_tests():
    print("Chạy kiểm tra API bằng thư viện requests...")

    for i, case in enumerate(test_cases):
        print(f"Test Case {i+1}: {case['name']}")
        print(f"Input Prompt: {case['prompt']}")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                API_URL, 
                json={
                    "prompt": case['prompt'], 
                    "max_new_tokens": case['max_new_tokens']
                },
                timeout=300 
            )
            
            if response.status_code == 200:
                result = response.json()
                elapsed = time.time() - start_time
                
                print(f"Thành công | Time: {round(elapsed, 2)}s")
                
                full_text = result.get("data", "")
                if "</think>" in full_text:
                    parts = full_text.split("</think>")
                    print(f"Câu trả lời của AI: {parts[-1].strip()}")
                else:
                    print(f"Câu trả lời của AI: {full_text}")
                
            else:
                print(f"Có lỗi | Code: {response.status_code}")
                print(f"Lỗi: {response.text}")

        except Exception as e:
            print(f"Không thể kết nối đến Server: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    run_tests()