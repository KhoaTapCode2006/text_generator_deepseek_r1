from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel, Field, field_validator
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import psutil
from datetime import datetime

app = FastAPI(title="Hệ thống AI Sinh Văn Bản (DeepSeek-R1)",
              description= "Hệ thống AI giúp tạo văn bản, câu trả lời dựa trên câu hỏi của bạn với tốc độ và độ chính xác cao")

MODEL_ID = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

print("Đang tải model, vui lòng đợi...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16, 
    low_cpu_mem_usage=True
)

print("Tải model thành công!")


class GenerationRequest(BaseModel):
    prompt: str =  Field(..., min_length=5, max_length=300, description="Prompt sinh văn bản")
    temperature: float = Field(0.6, ge=0, le=1.0)
    max_length: int = 300

    @field_validator('prompt')
    def prompt_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Prompt không được chỉ chứa khoảng trắng.')
        return v 

@app.get("/")
def read_root():
    return {
        "description": "Chào mừng bạn đến với hệ thống sinh văn bản bằng AI, hệ thống sử dụng mô hình DeepSeek Distil R1 gọn nhẹ với độ chính xác và sự sáng tạo cao.",
        "usage": "Gửi POST request đến /generate với JSON chứa 'prompt'.",
        "model_used": MODEL_ID,
        "note": "Hệ thống trả lời các câu prompt tốt nhất bằng tiếng Anh, các câu prompt nên có nội dung đầy đủ rõ ràng."
    }

@app.post("/generate")
def generate_text(request: GenerationRequest):

    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt không được để trống!")
    
    forbidden_words = ["nigga", "fuck", "hack"]
    if any(word in request.prompt.lower() for word in forbidden_words):
        raise HTTPException(status_code=403, detail="Prompt chứa nội dung hoặc từ ngữ không phù hợp.")

    try:

        userPrompt = f"<｜User｜>{request.prompt}<｜Assistant｜><think>\n"
        print(f"Đang sinh văn bản cho prompt: '{request.prompt}'...")
        inputs = tokenizer(userPrompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=1048,               
                do_sample=True,          
                temperature=0.6,         
                pad_token_id=tokenizer.eos_token_id,
                top_p=0.95,
                eos_token_id=tokenizer.eos_token_id
            )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if "</think>" in generated_text:
            final_answer = generated_text.split("</think>")[-1].strip()
        else:
            final_answer = generated_text 
            
        return {"status": "success", "data": final_answer}
    

    except torch.cuda.OutOfMemoryError:
        raise HTTPException(status_code=507, detail="Hệ thống quá tải bộ nhớ, vui lòng thử lại sau.")
    
    except Exception as e:
        print(f"Lỗi hệ thống: {e}") 
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi trong quá trình xử lý của mô hình AI."
        )

@app.get("/health")
def health_check():
    health_status = {
        "status": "Server hoạt động ổn.",
        "timestamp": datetime.now().isoformat(),
        "details": {}
    }
    
    try:
        mem = psutil.virtual_memory()
        health_status["details"]["memory"] = {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "percent_used": mem.percent
        }
        
        if 'model' in globals() and model is not None:
            health_status["details"]["model_loaded"] = True
            health_status["details"]["device"] = str(model.device)
        else:
            health_status["status"] = "Server đang gặp vấn đề về model!"
            health_status["details"]["model_loaded"] = False

        health_status["details"]["cpu_usage_percent"] = psutil.cpu_percent(interval=1)

    except Exception as e:
        health_status["status"] = "Server bị lỗi hoặc không thể kết nối!"
        health_status["details"]["error"] = str(e)

    return health_status