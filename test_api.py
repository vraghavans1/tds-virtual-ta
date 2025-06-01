import requests
import json

API_URL = "https://virtual-ta-eqsn.onrender.com/api/"
questions = [
    "What is the difference between Pandas and NumPy?",
    "How many quiz grades are dropped in this course?",
    "What do we submit for GA3 part 2?",
    "How do I fix a ModuleNotFoundError in Jupyter Notebook?",
    "Should I use gpt-4o-mini which AI proxy supports, or gpt3.5 turbo?"
]

print("🔍 Testing API...")

score = 0
for idx, question in enumerate(questions, 1):
    response = requests.post(API_URL, json={"question": question})
    print(f"Q{idx}: {question}")
    if response.status_code == 200:
        data = response.json()
        if "answer" in data and "links" in data:
            print("  ✅ Answer received")
            score += 1
        else:
            print("  ⚠️ Missing fields")
    else:
        print(f"  ❌ Error {response.status_code}")
print(f"✅ Test complete. Score: {score}/{len(questions)}")
