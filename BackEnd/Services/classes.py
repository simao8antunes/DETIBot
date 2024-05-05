from pydantic import BaseModel
class Source(BaseModel): # classe q define as fontes de conhecimento para dps serem guardadas na bd
    url: list[str] ####
    paths: list[str] ####
    loader_type: str
    update_period: str
    description: str
    wait_time: int ######
    recursive: bool #####

