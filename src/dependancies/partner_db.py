from src.db.partner_repo import PartnerRepo
from src.interfaces.partner_repo_interface import PartnerRepoInterface


def get_partner_db() -> PartnerRepoInterface:
    return PartnerRepo()
