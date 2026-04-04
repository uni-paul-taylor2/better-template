import uvicorn
from fastapi import FastAPI, Request, status, Form
from fastapi.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from app.config import get_settings
from app.dependencies import IsUserLoggedIn, SessionDep, AuthDep
from fastapi.templating import Jinja2Templates
from app.utilities import get_flashed_messages
from jinja2 import Environment, FileSystemLoader
from sqlmodel import select
from app.models import User, Album, Track, Comment, Reaction
from app.utilities import flash, create_access_token
from fastapi.staticfiles import StaticFiles


app = FastAPI(middleware=[
    Middleware(SessionMiddleware, secret_key=get_settings().secret_key)
]
)
template_env = Environment(loader = FileSystemLoader("app/templates",), )
template_env.globals['get_flashed_messages'] = get_flashed_messages
templates = Jinja2Templates(env=template_env)
static_files = StaticFiles(directory="app/static")

app.mount("/static", static_files, name="static")


@app.get('/', response_class=RedirectResponse)
async def index_view(
  request: Request,
  user_logged_in: IsUserLoggedIn,
):
  if user_logged_in:
    return RedirectResponse(url=request.url_for('home_view'), status_code=status.HTTP_303_SEE_OTHER)
  return RedirectResponse(url=request.url_for('login_view'), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login")
async def login_view(
  user_logged_in: IsUserLoggedIn,
  request: Request,
):
  if user_logged_in:
    return RedirectResponse(url=request.url_for('home_view'), status_code=status.HTTP_303_SEE_OTHER)
  return templates.TemplateResponse(
          request=request, 
          name="login.html",
      )

@app.post('/login')
def login_action(
  request: Request,
  db: SessionDep,
  username: str = Form(),
  password: str = Form(),
):
  
  user = db.exec(select(User).where(User.username == username)).one_or_none()
  if user and user.check_password(password):
    response = RedirectResponse(url=request.url_for("index_view"), status_code=status.HTTP_303_SEE_OTHER)
    access_token = create_access_token(data={"sub": f"{user.id}"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=False,
        samesite="lax",
        secure=True,
    )    
    return response
  else:
    flash(request, 'Invalid username or password')
    return RedirectResponse(url=request.url_for('login_view'), status_code=status.HTTP_303_SEE_OTHER)


@app.get('/app')
def home_view(request: Request, user: AuthDep, db: SessionDep):
  albums = db.exec(select(Album)).all()
  tracks = albums[0].tracks
  comments = tracks[0].comments
  return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
      "albums": albums,
      "tracks": tracks,
      "comments": comments,
      "reaction_count": len(tracks[0].reactions)
    }
  )

@app.get('/album/{album_id}')
def home_with_album(request: Request, user: AuthDep, db: SessionDep, album_id:int):
  albums = db.exec(select(Album)).all()
  tracks = db.exec(select(Album).where(Album.id==album_id)).first().tracks
  comments = tracks[0].comments
  return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
      "albums": albums,
      "tracks": tracks,
      "comments": comments,
      "reaction_count": len(tracks[0].reactions)
    }
  )

@app.get('/track/{track_id}')
def home_with_track(request: Request, user: AuthDep, db: SessionDep, track_id:int):
  track = db.exec(select(Track).where(Track.id==track_id)).first()
  comments = track.comments
  tracks = track.album.tracks
  albums = db.exec(select(Album)).all()
  return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
      "albums": albums,
      "tracks": tracks,
      "comments": comments,
      "reaction_count": len(track.reactions)
    }
  )

@app.get('/logout')
async def logout(request: Request):
  response = RedirectResponse(url=request.url_for("login_view"), status_code=status.HTTP_303_SEE_OTHER)
  response.delete_cookie(
      key="access_token", 
      httponly=True,
      samesite="none",
      secure=True
  )
  flash(request, 'logged out')
  return response