# main.py
from PurposeViewEnricher import PurposeViewEnricher

if __name__ == "__main__":
    input_file = "sample.json"  # Replace with your input JSON file path
    reference_file = "journal.json"  # Replace with your reference JSON file path
    output_dir = "output"  # Replace with your desired output directory
    PurposeViewEnricher.enrichView(input_file, reference_file, output_dir, 'COURT_JODGEMENT')
    