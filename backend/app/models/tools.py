from sqlmodel import Field, SQLModel


class Message(SQLModel):
    err: str = Field(..., description="Error code")
    message: str = Field(..., description="Full error message")


class ErrorMessage(SQLModel):
    detail: Message = Field(...)


responses = {400: {"model": ErrorMessage}}
