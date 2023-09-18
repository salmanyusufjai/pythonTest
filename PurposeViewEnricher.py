# json_enricher.py
import  pandas as pd
import json
import os
from EnricherFactory import EnricherFactory
from CompanyFinancialStatement import CompanyFinancialStatement

class PurposeViewEnricher:

    def enrichView(input_file, reference_file, output_dir, subdomain):
        if(subdomain == 'COMPANY_FINANCIAL_STATEMENT'):
            cfs = EnricherFactory.create_subdomain_enrich(input_file, reference_file, output_dir, subdomain)
            cfs.enrich_and_create_files()
        elif(subdomain == 'COURT_JODGEMENT'):
            cfs = EnricherFactory.create_subdomain_enrich(input_file, reference_file, output_dir, subdomain)
            cfs.enrich_and_create_files()
        elif(subdomain == 'COMPANY_REGISTER_LEGACY'):
            cfs = EnricherFactory.create_subdomain_enrich(input_file, reference_file, output_dir, subdomain)
            cfs.enrich_and_create_files()
        elif(subdomain == 'COMPANY_GAZETTE'):
            cfs = EnricherFactory.create_subdomain_enrich(input_file, reference_file, output_dir, subdomain)
            cfs.enrich_and_create_files()