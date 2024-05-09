from pydantic import BaseModel
class Source(BaseModel): # classe q define as fontes de conhecimento para dps serem guardadas na bd
    url: str
    paths: list[str] ####
    loader_type: str
    description: str
    wait_time: int = 3 #####
    recursive: bool = False#####
    update_period: str | int

