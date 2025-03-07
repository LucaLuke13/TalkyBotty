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


class telegram:
    def __init__(self, debug=False):
        # Load the .env file
        load_dotenv()

        # Access the variables
        api_id = os.getenv("TELEGRAM_API_ID")
        api_hash = os.getenv("TELEGRAM_API_HASH")
        session_name = os.getenv("SESSION_NAME")

        # Set up the argument parser
        parser = argparse.ArgumentParser(
            description="Telegram Voice Message Transcriber"
        )
        parser.add_argument(
            "-d", "--debug", action="store_true", help="Enable debug logging"
        )
        # args = parser.parse_args()

        # Set the debug level based on the command-line argument
        if True:
            logger.add(f"{session_name}.log", level="DEBUG")
        else:
            logger.add(f"{session_name}.log", level="INFO")

        logger.info("new session initialized")
        self.modelpath = os.getenv("MODEL_PATH")
        self.client = TelegramClient(session_name, api_id, api_hash)

        @self.client.on(events.NewMessage(incoming=True))
        async def handle_new_message(event):
            print(3456)
            # Check if the message has a video
            if event.message.video:
                print(f"Video received from {event.sender_id} and saved at")
                await self.process_video_message(event.message)
            # Check if the message has a voice note
            elif event.message.voice:
                await self.process_voice_message(event.message)

        self.client.start()
        self.client.run_until_disconnected()

    async def process_voice_message(self, voice_message):
        file_name = self.getFileNameForDownload(voice_message.sender_id, "ogg")
        await self.client.download_media(voice_message.media, file_name)
        wav_file_path = self.convert_ogg_to_wav(file_name)
        transcription = self.transcribe(wav_file_path)
        logger.debug(f"Received voice message from {voice_message.sender_id}")
        logger.debug("transcription:")
        logger.debug(transcription)
        if True:
            self.delete_file(file_name)
            self.delete_file(wav_file_path)
        message_chunks = self.split_message_to_chunks(transcription)
        print("message chunks:")
        print(message_chunks)
        for chunk in message_chunks:
            await voice_message.respond(chunk)

    async def process_video_message(self, video_message):
        file_name = self.getFileNameForDownload(video_message.sender_id, "mp4")
        logger.info("downloading video file " + file_name)
        await self.client.download_media(video_message.media, file_name)
        logger.info("download done")
        wav_file_path = self.convert_mp4_to_wav(file_name)
        transcription = self.transcribe(wav_file_path)
        logger.debug(f"Received voice message from {video_message.sender_id}")
        logger.debug("transcription:")
        logger.debug(transcription)
        if True:
            self.delete_file(file_name)
            self.delete_file(wav_file_path)
        message_chunks = self.split_message_to_chunks(transcription)
        for chunk in message_chunks:
            print(chunk)
            await video_message.respond(chunk)

    def split_message_to_chunks(self, input_string):
        # Define the maximum chunk size
        max_chunk_size = 4096
        if not input_string:
            return []
        # Split the input string into lines
        lines = input_string.split("\n")

        # Initialize an empty list to hold the chunks
        chunks = []

        # Initialize a temporary chunk and its size
        temp_chunk = ""
        temp_chunk_size = 0
        # Iterate over each line
        for line in lines:
            # Calculate the size of the new chunk if we add this line
            # Add  1 for the newline character if not the first line
            new_chunk_size = len(line) + temp_chunk_size

            # If adding this line would exceed the maximum chunk size, finalize the
            # current chunk and start a new one
            if new_chunk_size > max_chunk_size:
                chunks.append(temp_chunk)
                temp_chunk = line
                temp_chunk_size = len(line)
            else:
                # Otherwise, add the line to the current chunk
                if temp_chunk_size > 0:
                    temp_chunk += "\n" + line
                else:
                    temp_chunk += line
                temp_chunk_size = new_chunk_size

            logger.debug(len(line))
            logger.debug(new_chunk_size)
        # Append any remaining text as a final chunk
        if temp_chunk:
            chunks.append(temp_chunk)
        logger.debug("chunk size")
        logger.debug(chunks)
        return chunks

    def getFileNameForDownload(self, sender_id, extension):
        base_dir = "./data/voicemessages/telegram/"
        os.makedirs(base_dir, exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{sender_id}_{today}_{unique_id}.{extension}"
        return os.path.join(base_dir, filename)

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            logger.info(f"The file '{file_path}' has been removed successfully.")
        except FileNotFoundError:
            logger.error(f"The file '{file_path}' does not exist.")
        except PermissionError:
            logger.error(
                f"You do not have permission to delete the file '{file_path}'."
            )
        except Exception as e:
            logger.error(
                f"An error occurred while trying to delete the file '{file_path}': {e}"
            )

    def convert_ogg_to_wav(self, input_ogg_path):
        try:
            base_name = os.path.splitext(input_ogg_path)[0]
            output_wav_path = os.path.abspath(f"{base_name}.wav")
            audio = AudioSegment.from_ogg(input_ogg_path)
            resampled_audio = audio.set_frame_rate(16000).set_sample_width(2)
            resampled_audio.export(output_wav_path, format="wav")
            logger.info(f"Conversion successful. Output saved at {output_wav_path}")
            return output_wav_path
        except Exception as e:
            logger.error(f"An error occurred during conversion: {e}")

    def convert_mp4_to_wav(self, input_mp4_path):
        try:
            base_name = os.path.splitext(input_mp4_path)[0]
            output_wav_path = os.path.abspath(f"{base_name}.wav")

            # Load the video file
            clip = VideoFileClip(input_mp4_path)

            # Extract the audio track from the video
            audio = clip.audio

            # Write the audio to a WAV file
            audio.write_audiofile(output_wav_path)
            audio = AudioSegment.from_wav(output_wav_path)
            resampled_audio = audio.set_frame_rate(16000).set_sample_width(2)
            resampled_audio.export(output_wav_path, format="wav")
            logger.info(f"Conversion successful. Output saved at {output_wav_path}")
            return output_wav_path
        except Exception as e:
            logger.error(f"An error occurred during conversion: {e}")

    def transcribe(self, wav_file):
        whisper_path = os.path.abspath("./whisper.cpp/main")
        command = [
            whisper_path,
            "--model",
            self.modelpath,
            "--language",
            os.getenv("TRANSLATELANG"),
            "--file",
            "--translate",
            wav_file,
        ]
        print(command)
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0:
            return result.stdout
        else:
            logger.error(f"Command failed with error: {result.stderr}")
