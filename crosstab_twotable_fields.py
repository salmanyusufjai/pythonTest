from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def cross_tab_field_tables_binned(table1, table2, field):
    """
    Generate cross-tab of a field from two tables with bins: M, C, _, H, Other.
    
    Parameters:
    - table1, table2: BigQuery tables (project.dataset.table)
    - field: column name to compare
    
    Returns:
    - pivot_df: Pandas DataFrame with Table1 bins as rows, Table2 bins as columns
    """
    
    # Binning CASE for both tables
    bin_case = f"""
      CASE
        WHEN `{field}` = 'M' THEN 'M'
        WHEN `{field}` = 'C' THEN 'C'
        WHEN `{field}` = '_' THEN '_'
        WHEN `{field}` = 'H' THEN 'H'
        ELSE 'Other'
      END
    """
    
    # BigQuery query with binning
    query = f"""
    WITH t1_counts AS (
      SELECT {bin_case} AS t1_bin, COUNT(*) AS t1_count
      FROM `{table1}`
      GROUP BY t1_bin
    ),
    t2_counts AS (
      SELECT {bin_case} AS t2_bin, COUNT(*) AS t2_count
      FROM `{table2}`
      GROUP BY t2_bin
    )
    SELECT
      t1_bin,
      t2_bin,
      t1_count * t2_count AS joint_count
    FROM t1_counts
    CROSS JOIN t2_counts
    ORDER BY t1_bin, t2_bin
    """

    # Run query
    df = client.query(query).to_dataframe()

    # Pivot table: Table1 bins as rows, Table2 bins as columns
    pivot_df = df.pivot(index='t1_bin', columns='t2_bin', values='joint_count').fillna(0).astype(int)
    pivot_df.index.name = f"{field}_table1_bin"
    pivot_df.columns.name = f"{field}_table2_bin"

    return pivot_df



pivot = cross_tab_field_tables_binned(
    "myproject.mydataset.table1",
    "myproject.mydataset.table2",
    "status"
)

print(pivot)
