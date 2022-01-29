import json
import os
from pathlib import Path
from typing import Any

from aiopath import AsyncPath
from dotenv import load_dotenv


class BotConfig:

    def __init__(self) -> None:
        if os.path.isfile("config.env"):
            load_dotenv("config.env")

        config = {
            "api_id": os.environ.get("API_ID"),
            "api_hash": os.environ.get("API_HASH"),
            "bot_token": os.environ.get("BOT_TOKEN"),
            "db_uri": os.environ.get("DB_URI"),
            "download_path": os.environ.get("DOWNLOAD_PATH"),
            "gdrive_folder_id": os.environ.get("G_DRIVE_FOLDER_ID"),
            "gdrive_index_link": os.environ.get("G_DRIVE_INDEX_LINK"),
            "gdrive_secret": os.environ.get("G_DRIVE_SECRET"),
            "key_path": AsyncPath(Path.home() / ".cache" / "bot" / ".certs"),
            "owner": os.environ.get("OWNER")
        }

        for key, value in config.items():
            if value == "":
                value = 0 if key == "api_id" else None
            setattr(self, key, value)

    def __getattr__(self, name: str) -> Any:
        val = self.__getattribute__(name)
        if name == "download_path":
            return AsyncPath(val) if val else AsyncPath(Path.home() / "downloads")
        if name == "gdrive_index_link":
            return val.rstrip("/") if val is not None else val
        if name == "gdrive_secret":
            return json.loads(val) if val is not None else val

        return val

    def __getitem__(self, item: str) -> Any:
        return self.__getattr__(item)
