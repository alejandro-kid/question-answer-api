import os

SECRET_KEY = os.getenv("SECRET_KEY", "neO1Bhfajt")
LLMS_MODEL_PATH = os.getenv("LLMS_MODEL_PATH", "gpt4all-j-v1.3-groovy.bin")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")