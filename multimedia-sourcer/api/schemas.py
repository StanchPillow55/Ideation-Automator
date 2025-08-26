from typing import List,Optional,Dict,Any; from pydantic import BaseModel,Field; from models import SourceType
class SourceCreateJson(BaseModel): source_type:SourceType; url_or_path:Optional[str]=None; language:Optional[str]="en"
class DocumentOut(BaseModel): id:str; source_type:SourceType; url_or_path:Optional[str]; language:Optional[str]; class Config: from_attributes=True
class PipelineRunRequest(BaseModel): source_ids:List[str]; export_options:Optional[Dict[str,Any]]=Field(default_factory=dict)
class JobOut(BaseModel): job_id:str; status:str; stages:Dict[str,Any]; result:Dict[str,Any]=Field(default_factory=dict); error:Optional[str]=None
