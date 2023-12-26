import transformers
from peft import PeftConfig, PeftModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from config import MODEL_ID
from huggingface_hub import login

bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,  # 4-bit quantization
    bnb_4bit_quant_type='nf4',  # Normalized float 4
    bnb_4bit_use_double_quant=True,  # Second quantization after the first
    bnb_4bit_compute_dtype=torch.bfloat16  # Computation type
)

config = PeftConfig.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    torch_dtype=torch.float16,
    device_map="auto"
)
model = PeftModel.from_pretrained(
    model,
    MODEL_ID,
    torch_dtype=torch.float16
)
model.eval()

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=False)
generation_config = GenerationConfig.from_pretrained(MODEL_ID)
print(generation_config)

system_prompt = """
<s>[INST] <<SYS>>
Вы являетесь помощником, который предлагает рецепты на основе доступных ингредиентов.
<</SYS>>
"""

# Пример запроса
example_prompt = """
У меня есть следующие продукты: курица, помидоры, лук, чеснок.

Пожалуйста, предложите мне рецепт, используя эти ингредиенты.
[/INST] Курица в томатном соусе с чесноком и луком
"""

# Основной промпт
main_prompt = """
[INST]
У меня есть следующие продукты:
[PRODUCTS]

Пожалуйста, предложите мне рецепт, используя эти ингредиенты.
[/INST]
"""

generator = transformers.pipeline(
    model=MODEL_ID, tokenizer=tokenizer,
    task='text-generation',
    temperature=0.1,
    max_new_tokens=500,
    repetition_penalty=1.1
)


def request_recipe(products):
    product_list = ", ".join(products)
    prompt = system_prompt + example_prompt + main_prompt.replace("[PRODUCTS]", product_list)
    recipe_suggestion = generator(prompt)
    return recipe_suggestion
