# backend\accounts\validators.py
import re
from django.core.exceptions import ValidationError

# mobile e.g. +989xxxxxxxxx 
PHONE_REGEX = re.compile(r"^\+98(9\d{9})$")

# National ID without checksum algo
NATIONAL_ID_REGEX = re.compile(r"^\d{10}$")

# persian and eng letters and space
NAME_REGEX = re.compile(r"^[A-Za-z\u0600-\u06FF\s]+$")


def validate_phone_number(value: str):
    if not PHONE_REGEX.match(value):
        raise ValidationError("Phone number must be in format +98912xxxxxxx")


def validate_national_id_regex(value: str):
    if not NATIONAL_ID_REGEX.match(value):
        raise ValidationError("National ID must be exactly 10 digits")


def validate_name_only_letters(value: str):
    if not NAME_REGEX.match(value):
        raise ValidationError("Name must contain letters only (Persian/English)")

