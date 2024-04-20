import requests

BASE_URL = "http://localhost:8000"  # Replace with your actual application URL
def test_root():
    response = requests.get(f"{BASE_URL}/")  # Use requests library
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI!"}

def test_process_prompt():
    data = {
        "keyword": "남친",
        "content": "남친이랑 이별함",
        "mood": "절망",
        "additional": "남친의 이름은 이지우"
    }
    response = requests.post(f"{BASE_URL}/process-prompt", json=data)  # Use requests library
    assert response.status_code == 200
    print()
    print(f"/process-prompt 성공 응답: {response.json()}")  # 리턴값 출력

