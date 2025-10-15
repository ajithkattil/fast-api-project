from boto3 import client
from botocore.config import Config
from botocore.exceptions import ClientError

from src.core.config import settings
from src.core.exceptions import ServerError
from src.token_manager.models import Param, ParamResponse


class ParamStoreClient:
    def __init__(self) -> None:
        config = Config(
            region_name=settings.AWS_REGION,
        )
        self._client = client(
            "ssm",
            config=config,
        )

    def get_params(self, names: list[str]) -> list[Param]:
        if not names:
            return []

        try:
            response = self._client.get_parameters(Names=names, WithDecryption=True)
        except ClientError as e:
            raise ServerError("Failed to get parameters from Parameter Store") from e
        param_response = ParamResponse.model_validate(response)
        if param_response.invalid_parameters:
            raise ValueError(f"Invalid parameter names in request: {param_response.invalid_parameters}")

        for param_name in names:
            param = next((p for p in param_response.parameters if p.name == param_name), None)
            if param is None:
                raise ValueError(f"Parameter {param_name} not found in response")
        return list(param_response.parameters)

    def store_param(self, param: Param) -> None:
        try:
            self._client.put_parameter(
                Name=param.name,
                Value=param.value,
                Overwrite=True,
            )
        except ClientError as e:
            raise ServerError(f"Failed to store parameter {param.name} in Parameter Store") from e
