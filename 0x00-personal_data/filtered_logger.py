#!/usr/bin/env python3
""" Handling personal data """

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates fields in a log message using a single regex substitution.

    Args:
        fields: List of fields to obfuscate.
        redaction: String to replace the fields with.
        message: Log message to obfuscate.
        separator: Separator character between fields in the log message.

    Returns:
          The obfuscated log message.
          """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message
