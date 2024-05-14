from pydantic import BaseModel
class URL_Source(BaseModel): # classe q define as fontes de conhecimento para dps serem guardadas na bd
    url: str
    paths: list[str]
    update_period: str
    description: str
    wait_time: int  
    recursive: bool




class File_Source(BaseModel): # classe q define as fontes de conhecimento para dps serem guardadas na bd
    url: str
    loader_type: str
    update_period: str
    description: str