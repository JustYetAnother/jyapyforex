# test_script.py
from jyapyforex import ForexConverter
import os

# Ensure your API key is set in your environment before running this script
# For example: export FIXER_IO_API_KEY="YOUR_ACTUAL_FIXER_IO_API_KEY"

try:
    converter = ForexConverter()

    date = "2023-01-15"
    from_currency = "USD"
    to_currency = "EUR"

    rate = converter.get_conversion_rate(from_currency, to_currency, date)
    print(f"1 {from_currency} = {rate:.4f} {to_currency} on {date}")

    amount = 100.0
    converted_amount = converter.convert_amount(amount, from_currency, to_currency, date)
    print(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} on {date}")

except ValueError as e:
    print(f"Configuration Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")