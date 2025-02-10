import os
import warnings
from typing import Optional

import arxiv.config as arxiv_base

import logging
log = logging.getLogger(__name__)

class Settings(arxiv_base.Settings):
    TESTING: bool = True
    TEMPLATES_AUTO_RELOAD: Optional[bool] = None

    SQLALCHEMY_MAX_OVERFLOW: Optional[int] = 0
    SQLALCHEMY_POOL_SIZE: Optional[int] = 10

    FLASKS3_CDN_DOMAIN: str = "static.arxiv.org"
    FLASKS3_USE_HTTPS: bool = True
    FLASKS3_FORCE_MIMETYPE: bool = True
    FLASKS3_ACTIVE: bool = False

    def check(self) -> None:
        """A check and fix up of a settings object."""
        if 'sqlite' in self.CLASSIC_DB_URI:
            if not self.TESTING:
                log.warning(f"using SQLite DB at {self.CLASSIC_DB_URI}")
            self.SQLALCHEMY_MAX_OVERFLOW = None
            self.SQLALCHEMY_POOL_SIZE = None

        if (os.environ.get("FLASK_ENV", False) == "production"
                and "sqlite" in self.CLASSIC_DB_URI):
            warnings.warn(
                "Using sqlite in CLASSIC_DB_URI in production environment"
            )