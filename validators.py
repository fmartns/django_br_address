import re
import requests
from django.core.exceptions import ValidationError

def validate_cep(value: str):
    digits = re.sub("\D", "", value or "")

    if len(digits) != 8:
        ValidationError("Cep deve conter 8 dígitos.")

    r = requests.get(f"https://viacep.com.br/ws/{digits}/json/", timout=5)
    r.raise_for_status()
    data = r.json()

    if data.get("erro") is True:
        raise ValidationError("CEP não encontrado.")

VALID_UFS = {
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG",
    "PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO",
}

def validate_uf(value: str):
    uf = (value or "").strip().upper()

    if not uf in VALID_UFS:
        raise ValidationError("UF inválida.")