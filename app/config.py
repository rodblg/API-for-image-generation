from pydantic import BaseSettings

class Settings(BaseSettings):

    POSTGRES_USER:      str
    POSTGRES_PASSWORD:  str
    POSTGRES_HOST:      str
    POSTGRES_DB:        str
    OPENAI_APIKEY :     str
    SECRET_KEY:         str
    ALGORITHM:          str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    class Config:
        env_file = "C:\\Users\\rodri\\OneDrive\\Desktop\\Projects\\FastAPI_api\\.env"

settings = Settings()