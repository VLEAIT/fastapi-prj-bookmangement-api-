from pydantic_settings import  BaseSettings,SettingsConfigDict
from pydantic import AnyHTTPUrl,field_validator
from typing import List,Union



class Settings(BaseSettings):
    PROJECT_NAME:str="Book Tracker API"
    VERSION:str="v1.0"
    API_V1_STR:str="/api/v1"


    ALLOWED_ORIGIN:List[AnyHTTPUrl]
    DATABASE_URL:str
    SECRET_KEY:str
    PRODUCTION:bool=False

    @field_validator("ALLOWED_ORIGIN",mode="before")
    @classmethod
    def validate_origin(cls,value:Union[str,List[str]])->List[str]:
        if isinstance (value,list): 
            return value
        if isinstance(value,str):
            if value.startswith("[") and value.endswith("]"):
                return[item.strip("'/") for item in value[1:-1].split(",")]
            return[value.strip()] 
        raise ValueError("the data inserted is error ") 

    model_config=SettingsConfigDict(
            env_file=".env",
            case_sensetive=True,
            extra="ignore"
        )
settings=Settings()


