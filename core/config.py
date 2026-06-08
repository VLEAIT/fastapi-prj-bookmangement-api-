from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import LiST
from pydantic import AnyHTTPUrl,field_validator


class Settings(BaseSettings):
    PROJECT_NAME:str="Book Tracker API"
    VERSION:str="v1.0"
    API_V1_STR:str="/api/v1"


    ALLOWED_ORIGIN:List[AnyHTTPUrl]
    
    DATABSE_URL:str
    SECRET_KEY:str

    @field_validator("ALLOWED_ORIGIN", mode="before")
    @classmethod
    def  modify_origin(cls,value:Union[str,List[str]])->List[str]:
        if isinstance(value,list):
            return value
        if isinstance(value,str):
            if  value.startswith("[") and value.endswith("]"):
                return[item.strip(" '/")for item in value[1:-1].split(",")]
            return  [value.strip()]    
        raise ValueError("Invalid fomrat for origin") 

        model_config=SettingConfigDict(
            env_file=".env",
            case_sensitive=True,
            extra="ignore"
        )

settings=Settings()


