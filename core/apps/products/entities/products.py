from dataclasses import dataclass

import datetime


@dataclass
class Product:
    id: int
    title: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime