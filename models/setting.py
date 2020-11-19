from functools import lru_cache
from pydantic import BaseSettings


class APPSettings(BaseSettings):

    """ App setting """

    title: str = "Robots vs Dinosaurs"
    description: str = "A service that provides a REST API to support simulating an army \
                    of remote-controlled robots to fight the dinosaurs"
    version: str = "0.0.1"

    debug: bool = False

# Using cache to avoid loading setting configuration multiple times
@lru_cache()
def get_app_settings() -> APPSettings:
    return APPSettings()
