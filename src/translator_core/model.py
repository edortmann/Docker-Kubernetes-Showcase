import os
from functools import lru_cache
from typing import Tuple

import torch
from transformers import BitsAndBytesConfig, LlamaTokenizer, LlamaForCausalLM
from peft import PeftModel

_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

@lru_cache()
def _load() -> Tuple[LlamaTokenizer, PeftModel]:
    base = os.getenv("BASE_MODEL", "openlm-research/open_llama_3b_v2")
    adapter = os.getenv("ADAPTER_DIR", "weights/checkpoint-300")

    qcfg = BitsAndBytesConfig(load_in_4bit=True,
                              bnb_4bit_use_double_quant=True,
                              bnb_4bit_quant_type="nf4",
                              bnb_4bit_compute_dtype=torch.bfloat16)

    model = PeftModel.from_pretrained(
        LlamaForCausalLM.from_pretrained(base, quantization_config=qcfg),
        adapter,
        is_trainable=False
    ).to(_DEVICE)
    model.config.use_cache = True
    tok = LlamaTokenizer.from_pretrained(base)
    return tok, model

def translate(text: str, num_beams: int = 4) -> str:
    tok, model = _load()
    prompt = f"Translate from German to French: {text} ###>"
    inputs = tok(prompt, return_tensors="pt").to(_DEVICE)
    out = model.generate(**inputs,
                         max_new_tokens=100,
                         pad_token_id=model.config.eos_token_id,
                         num_beams=num_beams)[0]
    return tok.decode(out, skip_special_tokens=True).split("###>")[1].strip()
