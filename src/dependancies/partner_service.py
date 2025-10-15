from fastapi import Depends

from src.core.middleware.partner_id_middleware import partner_id_ctx
from src.dependancies.partner_db import get_partner_db
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.partner_service_interface import PartnerServiceInterface
from src.services.partner import PartnerService


def get_partner_service(
    partner_db: PartnerRepoInterface = Depends(get_partner_db),
) -> PartnerServiceInterface:
    partner_id = partner_id_ctx.get()
    if partner_id is None:
        raise ValueError("Partner ID not found in context")
    return PartnerService(partner_id=partner_id, partner_db=partner_db)
