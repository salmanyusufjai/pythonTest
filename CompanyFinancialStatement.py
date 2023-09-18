import  pandas as pd
import json
import os

class CompanyFinancialStatement:
    def __init__(self, input_file, reference_file, output_dir, subdomain):
            self.input_file = input_file
            self.reference_file = reference_file
            self.output_dir = output_dir
            self.subdomain = subdomain

    def enrich_and_create_files(self):

        input_df = pd.read_json(self.input_file)

        enriched_data = []

        for idx, row in input_df.iterrows():
            enriched_row = self.enrich_row(row, self.reference_file)
            input_df.at[idx, 'cfs']['latest'].append(enriched_row)

            enriched_data.append(row.to_dict())

        for idx, data in enumerate(enriched_data):
            self.create_json_file(data, idx)

    def enrich_row(self, row, reference_file):
        df = pd.read_json(reference_file)
        result = df[df.apply(lambda x: x['rawFields']['crn'] == row['cfs']['latest'][0]['rawFields']['crn'], axis=1)]
        newRow = row['cfs']['latest'][0]['pheder']
        target_dict = {
            "pheder": row['cfs']['latest'][0]['pheder']
        }
        
        print(newRow)
        if not result.empty:
            single_row_dict = result.iloc[0].to_dict()
            print(single_row_dict)
            target_dict.update(single_row_dict)
            return target_dict
        else:
            print("No matching rows found.")

    def create_json_file(self, data, idx):
        filename = os.path.join(self.output_dir, f"output_{idx}.json")
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
