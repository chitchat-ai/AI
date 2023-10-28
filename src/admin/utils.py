from fastapi import HTTPException

from .models import Config, PromptLog
from bson import ObjectId


async def list_configs(db, skip: int = 0, limit: int = 10):
    configs = await db["configs"].find().to_list(length=10000)
    return configs

async def get_config(db, config_id: str):
    config = await db["configs"].find_one({"_id": ObjectId(config_id)})
    if config:
        return Config(**config)
    return None

async def create_config(db, config: Config):
    config_dict = config.dict()
    result = await db["configs"].insert_one(config_dict)
    if result:
        return str(result.inserted_id)
    return None

async def update_config(db, config_id: str, config_data: Config):
    config_dict = config_data.dict()
    result = await db["configs"].update_one({"_id": ObjectId(config_id)}, {"$set": config_dict})
    if result:
        updated_config = await db["configs"].find_one({"_id": ObjectId(config_id)})
        if updated_config:
            return Config(**updated_config)
    return None

async def delete_config(db, config_id: str):
    result = await db["configs"].delete_one({"_id": ObjectId(config_id)})
    if result.deleted_count:
        return True
    return None

async def check_version_exists(db, version: str, exclude_id: str = None):
    query = {"version": version}
    if exclude_id:
        query["_id"] = {"$ne": ObjectId(exclude_id)}
    existing_config = await db["configs"].find_one(query)
    return bool(existing_config)

async def create_prompt_log(db, prompt_log: PromptLog):
    prompt_log_dict = prompt_log.dict()
    result = await db["prompt_logs"].insert_one(prompt_log_dict)
    if result:
        return str(result.inserted_id)
    return None

async def get_logs(db, sort_by: str = "chat_id", order: int = -1):
    logs = await db["prompt_logs"].find().to_list(length=10000)
    return logs