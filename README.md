# XML Data Processor

This project processes XML input files to extract and validate various parameters such as language, search type, date range, currency, nationality, and market. It applies business logic such as markup calculations and exchange rate conversions before returning a structured JSON response.

## Features

- Parses XML input data
- Validates required fields and applies default values where necessary
- Ensures start date is at least 2 days from today
- Ensures stay duration is at least 2 nights
- Handles currency conversion using predefined exchange rates
- Applies a markup percentage to the net price

## Prerequisites

- Python 3.6+

## Installation

1. Clone the repository:
   git clone <repository-url>
   pip install -r requirements.txt

## Usage

Run the script with an XML file (input.xml) as input:

python main.py

## License

This project is licensed under the MIT License.

