# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
class Project():
    def __init__(self, name, users):
        self.project_name = name
        self.project_users = users
        hash_id = name
        for i in users:
            hash_id += i.name
        self.id= hash(hash_id)
        self.ledger = pd.DataFrame({"project_id": self.id, 
                                    "transac_id": [np.nan],
                                    "date": [np.nan], 
                                    "total_amount": [np.nan],
                                    "people_name": [np.nan], 
                                    "payer_name": [np.nan], 
                                    "method": [np.nan],
                                    "description": [np.nan],
                                    "category": [np.nan]},
                                    dtype = 'object')
        self.balance = {user.name: 0 for user in users}
    
