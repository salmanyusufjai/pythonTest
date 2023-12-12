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
    avro_schema = avro_file.download_as_text(encoding='utf-8')
    
    with BytesIO(avro_file.download_as_bytes()) as avro_bytes:
        reader = DataFileReader(avro_bytes, avro.io.DatumReader())
        records = [record for record in reader]

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=[field['name'] for field in schema.fields])
        csv_writer.writeheader()
        
        for record in records:
            csv_writer.writerow(record)
