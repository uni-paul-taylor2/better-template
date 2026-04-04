import typer
from app.database import create_db_and_tables, get_cli_session, drop_all
from app.models import *
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from app.utilities import encrypt_password

cli = typer.Typer()

@cli.command("initialize")
def initialize():
    with get_cli_session() as db:
        drop_all() 
        create_db_and_tables() 
        
        bob = UserBase(username='bob', email='bob@mail.com', password=encrypt_password("bobpass"))
        bob_db = User.model_validate(bob)
        album_1 = Album(id=0,img="https://weblabs.web.app/api/brainrot/1.webp",title="Album 1",artist="man1")
        track_1 = Track(id=10,title="Song 10",album_id=0, album=album_1)
        track_2 = Track(id=11,title="Song 11",album_id=0, album=album_1)
        comment_1 = Comment(id=100,content="idk this song is peak",user_id=bob_db.id,user=bob_db,track_id=track_2.id,track=track_2)

        album_2 = Album(id=1,img="https://weblabs.web.app/api/brainrot/2.webp",title="Album 2",artist="man2")
        track_3 = Track(id=999,title="And Is Dat",album_id=1,album=album_2)
        reaction_1 = Reaction(id=998,user_id=bob_db.id,user=bob_db,track_id=track_3.id,track=track_3)

        db.add(bob_db)
        db.add(album_1)
        db.add(album_2)
        db.add(track_1)
        db.add(track_2)
        db.add(track_3)
        db.add(comment_1)
        db.add(reaction_1)
        db.commit()        
        print("Database Initialized")

@cli.command()
def test():
    print("You're already in the test")


if __name__ == "__main__":
    cli()