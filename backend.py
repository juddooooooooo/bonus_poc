import pandas as pd
from typing import Dict, Any

class BonusChecker:
    def __init__(self, db_path: str, terms_path: str):
        self.db_path = db_path
        self.terms_path = terms_path
        
        # 1. Load Database
        self.database = pd.read_csv(db_path, dtype={'account_id': str})
        
        # 2. Load Terms
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
            return {}
            
        return terms_dict

    def _get_terms_text(self, reason_code: str) -> str:
        return self.terms_mapping.get(reason_code, "Standard Terms & Conditions apply.")

    def check_status(self, account_id: str) -> Dict[str, Any]:
        account_id_stripped = str(account_id).strip()
        df = self.database
        
        # 1. Check if user exists
        user_row = df[df['account_id'] == account_id_stripped]
        
        if user_row.empty:
            return {
                "status": "error",
                "message": "Account Not Found",
                "details": "Please check your account number."
            }

        # 2. Extract Data
        user_data = user_row.iloc[0]
        
        # --- NEW LOGIC: VIP HOST CHECK ---
        # We check this FIRST. If they are hosted, we don't bother showing the standard bonus.
        if user_data.get('is_hosted', False):
            host_name = user_data.get('host_name', 'your VIP Manager')
            return {
                "status": "vip_redirect",
                "message": f"Welcome back, VIP!",
                "details": f"Your account is managed by **{host_name}**. Please contact them directly via WhatsApp or Email for your exclusive custom offers.",
                "action_url": "mailto:vip@betway.co.za" # Example link
            }
        
        # --- STANDARD LOGIC (For non-hosted players) ---
        reason_code = user_data['reason_code']
        terms_text = self._get_terms_text(reason_code)

        if user_data['is_eligible']:
            return {
                "status": "success",
                "message": f"Bonus Available: {user_data['bonus_value']} {user_data['currency']}",
                "details": terms_text,
                "action_url": "https://www.betway.co.za/lobby" # Redirect to Game Lobby
            }
        else:
            return {
                "status": "failed",
                "message": "Bonus Not Available",
                "details": terms_text,
                "action_url": "https://www.betway.co.za/lobby" # Redirect to Game Lobby
            }
