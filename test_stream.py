
import httpx

url = "http://127.0.0.1:8000/chat/stream"

data = {
    "question": "Explain minimum wages in India.",
    "language": "English"
}

with httpx.stream("POST", url, json=data, timeout=120) as response:
    print("Status:", response.status_code)

    for line in response.iter_lines():
        if line.startswith("data:"):
            print(line[5:].strip(), flush=True)
