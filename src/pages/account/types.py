from dataclasses import dataclass
from typing import Dict

from src.internals.types import PageProps
from src.types.account import Account

@dataclass
class AccountPageProps(PageProps):
    account: Dict
    currentPage: str = "account"
    title: str = "Your account page"

    def __post_init__(self):
        # TODO: remove after rewriting "load_account()" function.
        self.account = Account.init_from_dict(self.account)
