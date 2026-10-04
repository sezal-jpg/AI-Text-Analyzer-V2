import streamlit as st
import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

@st.cache_resource
def load_model():

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16)

    model.eval()

    return tokenizer, model

def generate_text(text):

    tokenizer, model = load_model()

    prompt = (
    "Complete the following text naturally and coherently.\n"
    "You are doing text completion, NOT answering a question.\n"
    "Continue directly from the last sentence.\n"
    "Write only new text that would naturally come after the input.\n"
    "Do not repeat any part of the input.\n"
    "Do not use labels such as 'Continuation:', 'Answer:', or 'Response:'.\n"
    "Do not ask the user questions.\n"
    "Do not give advice or recommendations.\n"
    "Do not introduce unrelated topics.\n"
    "Do not generate threats, harassment, intimidation, insults, profanity, or aggressive language.\n"
    "If the input is abusive, hostile, or inappropriate, continue it in a neutral and non-aggressive way.\n"
    "Do not escalate the tone of the input.\n"
    "Do not invent personal information or sensitive information.\n"
    "Only use information and context that is already present in the input.\n"
    "Complete your continuation with complete sentences.\n\n"
    "TEXT TO CONTINUE:\n"
    f"{text}\n\n"
    "Continue:"
)

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=60,
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
            
    if continuation:
        continuation=re.sub( r'\s+(Is there anything specific.*|Would you like.*|Do you want.*|Have you considered.*)$',
        '',continuation,flags=re.IGNORECASE).strip()
        
        last_end=max(continuation.rfind("."),
                     continuation.rfind("!"),
                     continuation.rfind('?'))   
        
        if last_end!=-1:
            continuation=continuation[:last_end+1].strip()  

    return continuation