from typing import List, Dict
from ..types.account import Account
from ..lib.pagination import Pagination

class Dashboard:
    def __init__(self,
    ) -> None:
        self.current_page = 'admin'

class Accounts:
    def __init__(self, 
        accounts: List[Account],
        role_list: List[str],
        pagination: Pagination
    ) -> None:
        self.current_page = 'admin'
        self.accounts = accounts
        self.role_list = role_list
        self.pagination = pagination
    
class Account_Props:
    def __init__(self,
        account: Account
    ) -> None:
        self.current_page = 'admin'
        self.account = account

class Account_Files:
    def __init__(self,
        account: Account,
        files: List[Dict]
    ) -> None:
        self.current_page = 'admin'
        self.account = account
        self.files = files

class ModeratorsActions():
    def __init__(self, 
        actions: List[Dict]
    ) -> None:
        self.current_page = 'admin'
        self.actions = actions

class Admin:
    def __init__(self) -> None:
        self.Dashboard = Dashboard
        self.Accounts = Accounts
        self.Account = Account_Props
        self.Account_Files = Account_Files
        self.ModeratorActions = ModeratorsActions


admin_props = Admin()
