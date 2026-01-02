import re
from django.core.exceptions import ValidationError
from .validators import validate_cep, validate_uf
from django.db import models

class CEPField(models.CharField):
    description = "CEP brasileiro (armazenado com 8 dígitos)"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 8)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if kwargs.get("max_length") == 8:
            del kwargs["max_length"]

        return name, path, args, kwargs

    def to_python(self, value):
        value = super().to_python(value)
        if value in (None, ""):
            return value

        return re.sub(r"\D", "", value)

    def get_prep_value(self, value):
        value = super().to_python(value)
        if value in (None, ""):
            return value
        validate_cep(value)
        return value

class UF(models.TextChoices):
    AC = "AC", "Acre"
    AL = "AL", "Alagoas"
    AP = "AP", "Amapá"
    AM = "AM", "Amazonas"
    BA = "BA", "Bahia"
    CE = "CE", "Ceará"
    DF = "DF", "Distrito Federal"
    ES = "ES", "Espírito Santo"
    GO = "GO", "Goiás"
    MA = "MA", "Maranhão"
    MT = "MT", "Mato Grosso"
    MS = "MS", "Mato Grosso do Sul"
    MG = "MG", "Minas Gerais"
    PA = "PA", "Pará"
    PB = "PB", "Paraíba"
    PR = "PR", "Paraná"
    PE = "PE", "Pernambuco"
    PI = "PI", "Piauí"
    RJ = "RJ", "Rio de Janeiro"
    RN = "RN", "Rio Grande do Norte"
    RS = "RS", "Rio Grande do Sul"
    RO = "RO", "Rondônia"
    RR = "RR", "Roraima"
    SC = "SC", "Santa Catarina"
    SP = "SP", "São Paulo"
    SE = "SE", "Sergipe"
    TO = "TO", "Tocantins"

class UFField(models.CharField):
    description = "Unidades Federais Brasileiras (armazenado com 2 digitos)"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 2)
        kwargs.setdefault("choices", UF.choices)
        super().__init__(*args, **kwargs)


    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if kwargs.get("max_length") == 2:
            del kwargs["max_length"]

        return name, path, args, kwargs

    def to_python(self, value):
        value = super().to_python(value)

        if value in (None, ""):
            return value

        return value.strip().upper()

    def get_prep_value(self, value):
        value = super().to_python(value)
        if value in (None, ""):
            return value
        validate_uf(value)
        return value