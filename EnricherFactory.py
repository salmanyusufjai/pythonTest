from CompanyGazette import CompanyGazette
from CompanyFinancialStatement import CompanyFinancialStatement
from CourtJudgment import CourtJudgment
from CompanyRegisterLegacy import CompanyRegisterLegacy
from SubdomainEnum import SubbdomainEnum


class EnricherFactory:
    def create_subdomain_enrich( input_file, reference_file, output_dir, subdomain):
        if subdomain == SubbdomainEnum.COMPANY_FINANCIAL_STATEMENT.name:
            return CompanyFinancialStatement(input_file, reference_file,output_dir,SubbdomainEnum.COMPANY_FINANCIAL_STATEMENT)
        elif subdomain == SubbdomainEnum.COMPANY_GAZETTE.name:
            return CompanyGazette(input_file, reference_file,output_dir,SubbdomainEnum.COMPANY_GAZETTE)
        elif subdomain == SubbdomainEnum.COMPANY_REGISTER_LEGACY.name:
            return CompanyRegisterLegacy(input_file, reference_file,output_dir,SubbdomainEnum.COMPANY_REGISTER_LEGACY)
        elif subdomain == SubbdomainEnum.COURT_JODGEMENT.name:
            return CompanyGazette(input_file, reference_file,output_dir,SubbdomainEnum.COURT_JODGEMENT)
        else:
            raise ValueError("Invalid subdomain type")
