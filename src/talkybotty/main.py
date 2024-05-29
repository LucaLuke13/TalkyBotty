from telethon import TelegramClient, events
import os
from datetime import datetime
import uuid
import subprocess
from pydub import AudioSegment
from dotenv import load_dotenv
from loguru import logger
import argparse
from moviepy.editor import VideoFileClip
from .classes.telegram import telegram

class talkyBotty:
    def run(args):
        tg = telegram(debug=args.debug)