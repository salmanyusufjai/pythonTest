from google.cloud import storage
import avro.schema
from avro.datafile import DataFileReader
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
    schema = avro.schema.parse(avro_file.download_as_text())
    
    with BytesIO(avro_file.download_as_bytes()) as avro_bytes:
        reader = DataFileReader(avro_bytes, avro.io.DatumReader())
        records = [record for record in reader]

    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=[field['name'] for field in schema.fields])
        csv_writer.writeheader()
        
        for record in records:
            csv_writer.writerow(record)

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
