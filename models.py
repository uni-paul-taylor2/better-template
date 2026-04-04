from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from pydantic import EmailStr
from pwdlib import PasswordHash

class UserBase(SQLModel,):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_comments: list['Comment'] = Relationship(back_populates="user")
    user_reactions: list['Reaction'] = Relationship(back_populates="user")

    def check_password(self, plaintext_password:str):
        return PasswordHash.recommended().verify(password=plaintext_password, hash=self.password)
    
class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    img: str = Field(default="")
    title: str = Field(default="")
    aritst: str = Field(default="")

    tracks: list['Track'] = Relationship(back_populates="album")

    def display(self):
        pass


class Track(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default="")
    album_id: int = Field(foreign_key="album.id")

    album: Album = Relationship(back_populates="tracks")
    comments: list['Comment'] = Relationship(back_populates="track")
    reactions: list['Reaction'] = Relationship(back_populates="track")

    def view_comments(self): #each comment by pull username
        pass

    def view_reactions(self): #count of reactions only
        pass


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(default="")
    user_id: int = Field(foreign_key="user.id")
    track_id: int = Field(foreign_key="track.id")

    track: Track = Relationship(back_populates="comments")
    user: User = Relationship(back_populates="user_comments")

    def delete(self):
        pass


class Reaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    like: bool = Field(default=True)
    user_id: int = Field(foreign_key="user.id")
    track_id: int = Field(foreign_key="track.id")

    track: Track = Relationship(back_populates="reactions")
    user: User = Relationship(back_populates="user_reactions")

    def react(self, type):
        self.like=bool(type)
