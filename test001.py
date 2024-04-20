import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel

app = FastAPI()

keyword = ""
content = ""
mood = ""
additional = ""

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

class PromptData(BaseModel):
    keyword: str
    content: str
    mood: str
    additional: str

prompt_data = PromptData(keyword='남친', content='남친이랑, 이별함', mood='절망', additional='남친의 이름은 이지우')

@app.post("/process-prompt")
def process_prompt(prompt_data: PromptData = Body()):
    prompt = f"{prompt_data.keyword}가 키워드인 {prompt_data.content}내용을 가지고 {prompt_data.mood}분위기를 가진 노래를 생성해줘 그런데 {prompt_data.additional}을 참고해서 노래 가사를 작성해주고 마지막에 제목도 정해줘"
    generated_text = generate(prompt)

    response = {
        "generated_text": generated_text
    }

    return response

def generate(prompt):
    vertexai.init(project="triple-backbone-334614", location="asia-northeast3")
    model = GenerativeModel("gemini-1.0-pro-vision-001")
    responses = model.generate_content(
        [prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    generated_text = ""

    for response in responses:
        generated_text += response.text

    # Serialize generated text to JSON
    json_response = {
        "generated_text": generated_text
    }

    # Return JSON response
    return json_response





generation_config = {
    "max_output_tokens": 2048,
    "temperature": 0.8,
    "top_p": 0.4,
    "top_k": 32,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
