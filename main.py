# main.py
from json_enricher import JsonEnricher

if __name__ == "__main__":
    input_file = "sample.json"  # Replace with your input JSON file path
    reference_file = "journal.json"  # Replace with your reference JSON file path
    output_dir = "output"  # Replace with your desired output directory

    enricher = JsonEnricher(input_file, reference_file, output_dir)
    enricher.enrich_and_create_files()
