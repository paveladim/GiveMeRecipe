import transformers
from torch import bfloat16
from config import MODEL_ID
from huggingface_hub import login


login(token = 'my token')
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,  # 4-bit quantization
    bnb_4bit_quant_type='nf4',  # Normalized float 4
    bnb_4bit_use_double_quant=True,  # Second quantization after the first
    bnb_4bit_compute_dtype=bfloat16  # Computation type
)

model_id = MODEL_ID
tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    # torch_dtype=torch.float16,  # Раскомментируйте для использования полупрецизионных вычислений
    trust_remote_code=True,
    quantization_config=bnb_config,
    device_map='auto',
)
model.eval()

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
    model=model, tokenizer=tokenizer,
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
