from pydantic import BaseModel

from models.domain.profiles import Profile


class ProfileInResponse(BaseModel):
    profile: Profile
