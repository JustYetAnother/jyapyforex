import requests
from datetime import datetime
from jyapyforex.exceptions import ForexAPIError, InvalidCurrencyError, RateNotFoundError

class FixerIOClient:
    """
    Client for interacting with the Fixer.io API to retrieve forex rates.
    Requires an API key from Fixer.io.
    """
    BASE_URL = "http://data.fixer.io/api/"

    def __init__(self, api_key: str):
        """
        Initializes the FixerIOClient with the provided API key.

        Args:
            api_key (str): Your API key for Fixer.io.
        """
        if not api_key:
            raise ValueError("Fixer.io API key cannot be empty.")
        self.api_key = api_key

    def get_historical_rate(self, date: str, base_currency: str, target_currency: str) -> float:
        """
        Fetches the historical exchange rate from Fixer.io for a specific date.

        Args:
            date (str): The date for which to retrieve the rate, in "YYYY-MM-DD" format.
            base_currency (str): The three-letter currency code for the base currency (e.g., "USD").
            target_currency (str): The three-letter currency code for the target currency (e.g., "EUR").

        Returns:
            float: The conversion rate from base_currency to target_currency on the given date.

        Raises:
            ValueError: If the date format is incorrect or currency codes are invalid.
            ForexAPIError: If there's an issue with the API request or response.
            RateNotFoundError: If the rate for the specified currencies/date is not available.
        """
        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: '{date}'. Expected YYYY-MM-DD.")
        
        # Fixer.io free plan typically uses EUR as base, so if base_currency is not EUR,
        # we might need to fetch EUR rates for both and then calculate.
        # For simplicity in this example, we assume the API supports the requested base,
        # but a more robust solution would handle base currency limitations.
        # Check Fixer.io documentation for your plan's base currency support.

        endpoint = f"{self.BASE_URL}{date}"
        params = {
            "access_key": self.api_key,
            "base": base_currency.upper(), # Ensure currency codes are uppercase
            "symbols": target_currency.upper()
        }
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            if not data.get("success"):
                error_info = data.get("error", {})
                error_code = error_info.get('code')
                error_type = error_info.get('type', 'UnknownError')
                error_message = error_info.get('info', 'No specific error information provided.')

                if error_code == 101: # Invalid API Key
                    raise ForexAPIError(f"Fixer.io API Error (Code {error_code}): Invalid API Key. {error_message}")
                elif error_code == 201: # Invalid base currency
                    raise InvalidCurrencyError(f"Fixer.io API Error (Code {error_code}): Invalid base currency '{base_currency}'. {error_message}")
                elif error_code == 202: # Invalid symbols
                    raise InvalidCurrencyError(f"Fixer.io API Error (Code {error_code}): Invalid target currency '{target_currency}'. {error_message}")
                elif error_code == 302: # Historical data not available for date
                    raise RateNotFoundError(f"Fixer.io API Error (Code {error_code}): Historical data not available for date '{date}'. {error_message}")
                else:
                    raise ForexAPIError(f"Fixer.io API Error ({error_type}, Code {error_code}): {error_message}")

            rates = data.get("rates", {})
            if target_currency.upper() in rates:
                return rates[target_currency.upper()]
            else:
                # This might happen if the API returns success but no rate for the specific symbol
                raise RateNotFoundError(f"Rate for {base_currency.upper()} to {target_currency.upper()} not found for {date}.")

        except requests.exceptions.Timeout:
            raise ForexAPIError(f"Fixer.io API request timed out after 10 seconds.")
        except requests.exceptions.ConnectionError:
            raise ForexAPIError(f"Could not connect to Fixer.io API. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise ForexAPIError(f"An unexpected request error occurred with Fixer.io: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            raise ForexAPIError(f"An unexpected error occurred while processing Fixer.io response: {e}")
