from google.cloud import storage
from avro.datafile import DataFileReader
from avro.io import DatumReader
import csv
from io import BytesIO

def read_avro_from_gcs(bucket_name, folder_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    avro_files = []
    
    # List all files in the folder
    blobs = bucket.list_blobs(prefix=folder_path)
    
    for blob in blobs:
        if blob.name.endswith('.avro'):
            avro_files.append(blob)
    
    return avro_files

def avro_to_csv(avro_file, csv_file):
    with BytesIO(avro_file.download_as_bytes()) as avro_bytes:
        reader = DataFileReader(avro_bytes, DatumReader())
        records = [record for record in reader]

    # Write header only if the CSV file doesn't exist
    write_header = not avro_file_exists(csv_file)

    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=[key for key in records[0].keys()])

        if write_header:
            csv_writer.writeheader()

        for record in records:
            cleaned_record = {key: str(value) for key, value in record.items()}
            csv_writer.writerow(cleaned_record)

def avro_file_exists(file_path):
    try:
        with open(file_path, 'r') as file:
            # Try to read the first line to check if the file exists and has content
            file.readline()
        return True
    except FileNotFoundError:
        return False

def main():
    # Replace these with your actual values
    input_bucket = "your-input-bucket"
    input_folder = "your-input-folder"
    output_csv_file = "output.csv"

    avro_files = read_avro_from_gcs(input_bucket, input_folder)

    for avro_file in avro_files:
        avro_to_csv(avro_file, output_csv_file)

if __name__ == "__main__":
    main()
