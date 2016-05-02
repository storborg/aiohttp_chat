from sqlalchemy import create_engine

from .base import *
from .message import *
from .utils import *


def init(url):
    engine = create_engine(url)
    Session.configure(bind=engine)
    Base.metadata.bind = engine
