from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname:str
    database_name: str
    database_username: str
    database_password:str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes:int
    google_client_id: str
    google_client_secret:str
    google_redirect_url: str
    model_config = {'env_file': '.env'}






settings = Settings()

