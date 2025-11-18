from google.cloud import bigquery

client = bigquery.Client()

def generate_field_profile_with_total(table):
    # 1. Get column names from BigQuery table
    table_ref = client.get_table(table)
    columns = [schema.name for schema in table_ref.schema if schema.field_type != "RECORD"]

    queries = []

    # 2. Build a subquery for each column
    for col in columns:
        q = f"""
        SELECT 
          '{col}' AS field_name,
          COUNTIF({col} = 'M') AS M,
          COUNTIF({col} = 'C') AS C,
          COUNTIF({col} = '_') AS underscore,
          COUNTIF({col} = 'H') AS H,
          COUNTIF({col} NOT IN ('M','C','_','H') AND {col} IS NOT NULL) AS Other,
          COUNT(*) AS total_records
        FROM `{table}`
        """
        queries.append(q)

    # 3. UNION ALL all column queries
    final_query = " UNION ALL ".join(queries)

    print("Running Query...\n", final_query[:500] + " ...")  # show first 500 chars
    return client.query(final_query).to_dataframe()


# ------------------------------
# Example usage
# ------------------------------
df = generate_field_profile_with_total("myproject.mydataset.mytable")
print(df)
