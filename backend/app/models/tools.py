from sqlmodel import Field, SQLModel


class Message(SQLModel):
    type: str = Field(..., description="Error code")
    msg: str = Field(..., description="Full error message")


class ErrorMessage(SQLModel):
    detail: Message = Field(...)


responses = {400: {"model": ErrorMessage}}
