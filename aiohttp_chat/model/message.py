from sqlalchemy import Table, Column, types

from . import utils
from .base import Base, Session

__all__ = ['Message']


class Message(Base):
    """
    A chat message.
    """
    __tablename__ = 'messages'
    id = Column(types.Integer, primary_key=True)
    sender_name = Column(types.Unicode(255), nullable=False)
    remote_addr = Column(types.String(255), nullable=False)
    body = Column(types.UnicodeText, nullable=False)
    sent_time = Column(types.DateTime, nullable=False, default=utils.utcnow)


def log_message(sender_name, remote_addr, body):
    msg = Message(sender_name=sender_name,
                  remote_addr=remote_addr,
                  body=body)
    Session.add(msg)
    Session.commit()
