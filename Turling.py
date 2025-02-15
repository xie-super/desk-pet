import google.generativeai as genai
# transport需要加上否则超时
genai.configure(api_key="AIzaSyD0hIP0V0uxnySVWE3yvXnkGAxb4Fxk2ao",transport='rest')

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)
def Tuling(words):
  response = chat_session.send_message(words+"")
  return response.text

if __name__ == "__main__":
  res = Tuling("介绍一下端午节，1000字")
  print(res)