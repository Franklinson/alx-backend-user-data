#!/usr/bin/env python3
""" Handling personal data """

import re


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    return re.sub(fr'(?<=\b({"|".join(fields)})\b{separator})[^\{separator}]*',
                  redaction, message)
