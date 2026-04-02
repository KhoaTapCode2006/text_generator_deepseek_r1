# 🤖 HỆ THỐNG SINH VĂN BẢN BẰNG MÔ HÌNH DEEPSEEK-R1 🤖
___
# MÔ TẢ:
Hệ thống sinh văn bản được xây dựng bằng FastAPI và model AI của Hugging Face. Hệ thống 
chứa các tính năng cơ bản cho việc sinh văn bản bằng AI một cách thông minh và sáng tạo.
Với model DeepSeek-R1 chứa 1.5 tỷ params, các câu lệnh sinh văn bản sẽ được thực hiện dễ
dàng và nhanh chóng. Ngoài ra, hệ thống còn có thể viết code, làm toán, trò chuyện,....
___
+ **Tên mô hình AI:** DeepSeek-R1-Distill-Qwen-1.5B
+ **Liên kết:** *[Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)*
+ **Chức năng:** Hệ thống sinh văn bản, viết code, làm toán, trò chuyện dựa trên yêu cầu đẩy đủ ngữ cảnh, nội dung của người dùng 1 cách nhanh chóng, tiện lợi và thông minh.

___
# CÁCH CÀI THƯ VIỆN
+ Bước 1: Mở 1 Code Editor và mở 1 terminal mới
+ Bước 2: Gõ lệnh vào terminal: pip install fastapi uvicorn transformers torch pydantic
+ Bước 3: Chờ cài đặt xong
___
# HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH
**CÁCH 1: SỬ DỤNG SWAGGER UI**
+ Bước 1: Mở 1 Code Editor và mở 1 terminal mới
+ Bước 2: Gõ lệnh vào terminal: uvicorn main:app --reload
+ Bước 3: Vào đường link http://127.0.0.1:8000/docs
+ Bước 4: Sử dụng trực tiếp các tính năng GET, POST 
+ GET \, \health: Để lấy thông tin mô tả hoặc trạng thái của hệ thống
+ POST \generate: Để thực hiện việc viết lệnh sinh văn bản cho hệ thống

**CÁCH 2: SỬ DỤNG GIAO DIỆN STREAMLIT**
+ Bước 1: Mở 1 Code Editor và mở 1 terminal mới
+ Bước 2: Gõ lệnh vào terminal: uvicorn main:app --reload
+ Bước 3: Chạy chương trình app.py trên terminal bằng lệnh: streamlit run app.py
+ Bước 4: Sử dụng như các ứng dụng ChatGPT, Gemini,...
___
# CÁCH GỌI API VÀ VÍ DỤ RESPONSE/REQUEST
**Các thành phần trong lệnh gọi API:**
+ URL/Endpoint: http://127.0.0.1:8000
+ Method: GET, POST
+ Headers: File JSON
+ Body: Câu prompt kiểu string

**Cách gọi API:**
+ Bước 1: Mở Code Editor, vào phần terminal và chạy server bằng lệnh: uvicorn main:app --reload
+ Bước 2: Chạy lệnh trong terminal (Lưu ý: max_new_tokens nên để từ 512 -> 1024):
+ Bước 3: Câu trả lời sẽ chứa trong file output.json trong thư mục chứa main.py
~~~
$data = @{ prompt = "Write a python code to calculate sum of 2 numbers."; max_new_tokens = 512 } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/generate" `
                              -Method Post `
                              -Body ([System.Text.Encoding]::UTF8.GetBytes($data)) `
                              -ContentType "application/json; charset=utf-8"
$response | ConvertTo-Json | Out-File -FilePath "output.json" -Encoding utf8
Write-Host "Đã lưu kết quả vào file output.json" -ForegroundColor Green
~~~

**Ví dụ về request:**
```
{
  "prompt": "Write me a short essay about the computer",
  "temperature": 0.6,
  "max_length": 300
}
```

**Ví dụ về response:**
```
{
  "status": "success",
  "data": "**The Impact of Computers: A Comprehensive Overview**\n\nIn the vast landscape of technology, computers stand as a testament to human ingenuity and the evolution of information processing...." 
}
```


