from pydantic import BaseModel
class Source(BaseModel): # classe q define as fontes de conhecimento para dps serem guardadas na bd
    url: str
    loader_type: str
    update_period: str
    description: str
