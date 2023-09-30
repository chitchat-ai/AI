from fastapi import APIRouter, Depends, HTTPException, Form, Query
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status

from settings import settings
from src.admin.utils import list_configs, get_config, create_config, update_config, delete_config, \
    check_version_exists, get_logs
from src.admin.models import Config
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.database import get_database

security = HTTPBasic()
def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = settings.ADMIN_USERNAME
    correct_password = settings.ADMIN_PASSWORD
    if credentials.username == correct_username and credentials.password == correct_password:
        return "admin"  # Return a value indicating an admin is authenticated
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

config_router = APIRouter(
    prefix="/configs",
    tags=["configs"],
    dependencies=[Depends(get_current_admin)],
)

templates = Jinja2Templates(directory="templates")

@config_router.get("/")
async def read_configs(request: Request, skip: int = 0, limit: int = 10, db=Depends(get_database)):
    configs = await list_configs(db, skip, limit)
    return templates.TemplateResponse("configs.html", {"request": request, "configs": configs})

@config_router.get("/create")
async def create_config_form(request: Request):
    return templates.TemplateResponse("create_config.html", {"request": request})

@config_router.post("/")
async def create_configs(
    version: str = Form(...),
    prompt_template: str = Form(...),
    temperature: float = Form(...),
    db=Depends(get_database)
):
    if await check_version_exists(db, version):
        raise HTTPException(status_code=400, detail="Version already exists")
    config_data = Config(
        version=version,
        prompt_template=prompt_template,
        temperature=temperature
    )
    await create_config(db, config_data)
    return RedirectResponse(url="/configs/", status_code=303)

@config_router.get("/{config_id}/edit")
async def edit_config_form(request: Request, config_id: str, db=Depends(get_database)):
    config = await get_config(db, config_id)
    if config:
        return templates.TemplateResponse("edit_config.html", {"request": request, "config": config, "config_id": config_id})
    raise HTTPException(status_code=404, detail="Config not found")

@config_router.post("/{config_id}")
async def update_configs(
    config_id: str,
    version: str = Form(...),
    prompt_template: str = Form(...),
    temperature: float = Form(...),
    db=Depends(get_database)
):
    config_data = Config(
        version=version,
        prompt_template=prompt_template,
        temperature=temperature
    )
    updated_config = await update_config(db, config_id, config_data)
    if updated_config:
        return RedirectResponse(url="/configs/", status_code=303)
    raise HTTPException(status_code=404, detail="Config not found")

@config_router.get("/{config_id}/delete")
async def delete_configs(config_id: str, db=Depends(get_database)):
    deleted_config = await delete_config(db, config_id)
    if deleted_config:
        return RedirectResponse(url="/configs/", status_code=303)
    raise HTTPException(status_code=404, detail="Config not found")

logs_router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    dependencies=[Depends(get_current_admin)],
)

@logs_router.get("/")
async def list_logs(
    request: Request,
    # sort_by: str = Query("chat_id", description="Field to sort by"),
    # order: str = Query("asc", description="Sorting order ('asc' or 'desc')"),
    db=Depends(get_database)
):
    logs = await get_logs(db)
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})
