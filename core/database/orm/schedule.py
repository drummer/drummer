#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from core.database.sessions import SqliteSession
from core.database import Base

SHORT_STRING = 30
LONG_STRING  = 400

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)

    # job name
    name = Column(String(SHORT_STRING), nullable=False)

    # job description
    description = Column(String(LONG_STRING), nullable=False)

    # cron expression
    cronexp = Column(String(SHORT_STRING), nullable=False)

    # job parameters including task parameters and task chain
    parameters = Column(String(LONG_STRING), nullable=True)

    # enabled
    enabled = Column(Boolean, nullable=False, default=True)
