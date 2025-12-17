import pandas as pd
from typing import Dict, Any

class BonusChecker:
    def __init__(self, db_path: str, terms_path: str):
        self.db_path = db_path
        self.terms_path = terms_path
        
        # 1. Load Database
        self.database = pd.read_csv(db_path, dtype={'account_id': str})
        
        # 2. Load Terms into a dictionary
        self.terms_mapping = self._load_terms_to_dict()

    def _load_terms_to_dict(self):
        terms_dict = {}
        current_code = None
        current_text = []

        try:
            with open(self.terms_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line: continue 
                    
                    if line.startswith('[') and line.endswith(']'):
                        if current_code:
                            terms_dict[current_code] = " ".join(current_text)
                        
                        current_code = line[1:-1]
                        current_text = []
                    else:
                        current_text.append(line)
                
                if current_code:
                    terms_dict[current_code] = " ".join(current_text)
                    
        except FileNotFoundError:
            print(f"Warning: {self.terms_path} not found.")
            
        return terms_dict

    def _get_terms_text(self, reason_code: str) -> str:
        """
        Looks up the code in our loaded dictionary.
        """
        return self.terms_mapping.get(reason_code, "Standard Terms & Conditions apply.")

    def check_status(self, account_id: str) -> Dict[str, Any]:
        account_id_stripped = str(account_id).strip()
        df = self.database
        
        user_row = df[df['account_id'] == account_id_stripped]
        
        if user_row.empty:
            return {
                "status": "error",
                "message": "Account Not Found",
                "details": "Please check your account number and try again."
            }

        user_data = user_row.iloc[0] 
        reason_code = user_data['reason_code']
        terms_text = self._get_terms_text(reason_code)

        # 3. Scenario: Eligible
        if user_data['is_eligible']:
            return {
                "status": "success",
                "message": f"Bonus Available: {user_data['bonus_value']} {user_data['currency']}",
                "details": terms_text
            }
        
        # 4. Scenario: Not Eligible
        else:
            return {
                "status": "failed",
                "message": "Bonus Not Available",
                "details": terms_text 
            }