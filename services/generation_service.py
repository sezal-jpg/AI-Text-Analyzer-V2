import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

@st.cache_resource
def load_model():

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32 )

    model.eval()

    return tokenizer, model

def generate_text(text):

    tokenizer, model = load_model()

    prompt = (
        "Continue the following text naturally.\n"
        "Write only the continuation.\n"
        "Do not repeat the original text.\n"
        "Do not answer the user.\n"
        "Do not say hello.\n"
        "Do not give advice.\n"
        "Do not mention that you are an AI assistant.\n"
        "Stay on the same topic.\n"
        "Do not introduce unrelated facts, companies, "
        "technologies, or information.\n\n"
        "TEXT:\n"
        f"{text}\n\n"
        "CONTINUATION:"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=40,
            do_sample=True,
            temperature=0.65,
            top_p=0.85,
            top_k=30,
            repetition_penalty=1.15,
            no_repeat_ngram_size=3,
        )

    generated_tokens = outputs[
        0
    ][
        inputs["input_ids"].shape[1]:
    ]

    continuation = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    for prefix in [
        "CONTINUATION:",
        "Continuation:",
        "continuation:"]:
        if continuation.startswith(prefix):
            continuation = continuation[len(prefix):].strip()

    return continuation