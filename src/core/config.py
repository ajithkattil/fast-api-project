from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    PROJECT_NAME: str = Field(default="Recipes API")
    APP_NAME: str = Field(default="Recipes api")
    VERSION: str = Field(default="0.1.0")
    AWS_REGION: str = Field(default="us-east-1")
    LOG_DIR: str = Field(default="logs")
    LOG_LEVEL: str = Field(default="INFO")
    BASE_URL: str = Field(default="http://localhost:8000")
    DEFAULT_PAGE_SIZE: int = Field(default=100)
    DATABASE_URL: str
    DATABASE_NAME: str = Field(default="recipes_api_service_primary")
    DATABASE_USER: str = Field(default="recipes_api_service_primary")
    DATABASE_PASSWORD: str = Field(validation_alias="SERVICE_DATABASE_PASSWORD")
    DATABASE_PORT: str = Field(default="5432")
    DEPLOY_ENV: str = Field(default="dev")
    IDEMPOTENCY_KEY_TTL_MINUTES: int = Field(default=1440)
    SECRET_KEY: str = Field(default="secret")
    TOKEN_ALGORITHM: str = Field(default="HS256")
    TOKEN_EXPIRES_IN: int = Field(default=3600)  # 1 hour
    TOKEN_ISSUER_SVC_NAME: str = Field(default="recipes-api-service")
    CUL_OPS_AUDIENCE: str = Field(default="culinary-operations-server")
    MAX_PAGE_SIZE: int = Field(default=500, description="Maximum number of items per page for any paginated endpoint")
    CULOPS_API_HOST: str = Field(default="culinary-operations-server.staging.f--r.co")
    MOCK_CULOPS_API: bool = Field(default=True, description="Use mocked CulOps API responses")
    CABINET_API_HOST: str = Field(default="cabinet.staging.f--r.co")
    MOCK_CABINET_API: bool = Field(default=True, description="Use mocked Cabinet API responses")
    KAFKA_BOOTSTRAP_SERVER: str = Field(default="localhost:9092")
    KAFKA_PRODUCER_GET_TIMEOUT: int = Field(
        default=6,
        description="Client-side timeout in seconds for waiting on a synchronous Kafka produce call to complete.",
    )
    FULFILLMENT_TOPIC: str = Field(default="fes-async-in")
    FES_GRPC_HOST: str = Field(default="fulfillment-engine-grpc.wms.svc.cluster.local")
    GRPC_PORT: int = Field(default=50051)
    FULFILLMENT_RESPONSE_TOPIC: str = Field(default="fes-async-out")

    ROLLBAR_SERVER_TOKEN: str | None = Field(default=None)
    ROLLBAR_CLIENT_TOKEN: str | None = Field(default=None)
    ROLLBAR_ENV: str | None = Field(default=None)
    ROLLBAR_CODE_VERSION: str | None = Field(default=None)

    # Connect
    CONNECT_CLIENT_ID: str
    CONNECT_CLIENT_SECRET: str
    CONNECT_RETRY_COUNT: int = Field(default=3)

    # Parameter Store
    SERVICE_PARAMS_BASE_PATH: str = Field(default="applications/wms/recipes-api-service/environment")
    CUL_OPS_ACCESS_TOKEN_PARAM_NAME: str = Field(default="CUL_OPS_ACCESS_TOKEN")
    CUL_OPS_REFRESH_TOKEN_PARAM_NAME: str = Field(default="CUL_OPS_REFRESH_TOKEN")

    # Token
    TOKEN_EXPIRY_BUFFER: int = Field(default=300)  # 5 minutes - triggers refresh before CronJob cycle

    # CulOps client config
    CULOPS_PANTRY_FETCH_SIZE: int = Field(default=100)

    # Database connection pooling
    DB_POOL_SIZE: int = Field(default=20, description="SQLAlchemy connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=10, description="SQLAlchemy max overflow connections")
    DB_POOL_TIMEOUT: int = Field(default=30, description="Connection pool timeout in seconds")


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
