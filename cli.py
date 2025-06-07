# This file defines the command-line interface (CLI) for the library.
# It allows users to interact with the library directly from the terminal.

import argparse
import sys
import logging
from jyapyforex import ForexConverter, __version__
from jyapyforex.exceptions import ForexAPIError, InvalidCurrencyError, RateNotFoundError
from jyapyforex.utils import logger as lib_logger, validate_date_format, validate_currency_code

# Configure the root logger for CLI output.
# Basic configuration sends messages to console.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    """
    Main function for the command-line interface.
    Parses arguments and calls the appropriate ForexConverter methods.
    """
    parser = argparse.ArgumentParser(
        prog="jyapyforex", # The name of your command
        description="A Python library for fetching historical forex rates and converting currencies.",
        epilog="Remember to set your API keys as environment variables (e.g., FIXER_IO_API_KEY)."
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging for more detailed output."
    )

    # Subparsers for different commands (rate, convert, etc.)
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # --- 'rate' command ---
    rate_parser = subparsers.add_parser(
        "rate",
        help="Get the conversion rate between two currencies for a specific date.",
        formatter_class=argparse.RawTextHelpFormatter # For better formatting of help text
    )
    rate_parser.add_argument("from_currency", type=str, help="Source currency code (e.g., USD).")
    rate_parser.add_argument("to_currency", type=str, help="Target currency code (e.g., EUR).")
    rate_parser.add_argument("date", type=str, help="Date in YYYY-MM-DD format (e.g., 2023-01-15).")
    rate_parser.set_defaults(func=handle_rate_command)

    # --- 'convert' command ---
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert an amount from one currency to another for a specific date.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    convert_parser.add_argument("amount", type=float, help="Amount to convert.")
    convert_parser.add_argument("from_currency", type=str, help="Source currency code (e.g., USD).")
    convert_parser.add_argument("to_currency", type=str, help="Target currency code (e.g., EUR).")
    convert_parser.add_argument("date", type=str, help="Date in YYYY-MM-DD format (e.g., 2023-01-15).")
    convert_parser.set_defaults(func=handle_convert_command)

    args = parser.parse_args()

    # Set logging level based on --debug flag
    if args.debug:
        lib_logger.setLevel(logging.DEBUG) # Set logging for your library's modules
        logging.getLogger().setLevel(logging.DEBUG) # Set logging for the root logger (CLI output)
        logging.debug("Debug logging enabled.")

    # Execute the chosen command handler
    if args.command:
        try:
            # Initialize ForexConverter once for all commands that need it
            # This will attempt to load API keys from environment variables
            converter = ForexConverter()
            args.func(converter, args)
        except (ValueError, ForexAPIError, InvalidCurrencyError, RateNotFoundError) as e:
            logging.error(f"Error: {e}")
            sys.exit(1) # Exit with an error code
        except Exception as e:
            # Catch any unexpected Python errors
            logging.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
            sys.exit(1)
    else:
        # This part should theoretically not be reached if required=True for subparsers,
        # but kept as a fallback.
        parser.print_help()


def handle_rate_command(converter: ForexConverter, args: argparse.Namespace):
    """Handler for the 'rate' command."""
    # The validations in utils.py will raise ValueError, which is caught by main()
    validate_currency_code(args.from_currency)
    validate_currency_code(args.to_currency)
    validate_date_format(args.date)

    rate = converter.get_conversion_rate(args.from_currency.upper(), args.to_currency.upper(), args.date)
    logging.info(f"1 {args.from_currency.upper()} = {rate:.4f} {args.to_currency.upper()} on {args.date}")

def handle_convert_command(converter: ForexConverter, args: argparse.Namespace):
    """Handler for the 'convert' command."""
    if args.amount < 0:
        raise ValueError("Amount cannot be negative.")
    # The validations in utils.py will raise ValueError, which is caught by main()
    validate_currency_code(args.from_currency)
    validate_currency_code(args.to_currency)
    validate_date_format(args.date)

    converted_amount = converter.convert_amount(args.amount, args.from_currency.upper(), args.to_currency.upper(), args.date)
    logging.info(f"{args.amount:.2f} {args.from_currency.upper()} = {converted_amount:.2f} {args.to_currency.upper()} on {args.date}")


if __name__ == "__main__":
    # This block allows you to run cli.py directly for testing:
    # python src/my_forex_library/cli.py rate USD EUR 2023-01-15
    main()