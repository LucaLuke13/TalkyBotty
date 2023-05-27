
TalkyBotty utilizes `whisper.cpp` to transcribe and translate voice messages and videos with a telegram bot. Stop sending me voice and video messages.

## How to Use

Simply forward a video or voice message in any language to the bot, and it will reply with a translation.

## Installation Guide for Admins

### Prerequisites

Ensure you have Git installed on your system.

### Steps to Install

1. Clone the repository:
```bash
git clone git@github.com:LucaLuke13/TalkyBotty.git
```

2. Navigate to the cloned directory:
```bash
cd TalkyBotty
```

3. Initialize the environment and install dependencies:
```bash
bash init_whisper.cpp.sh
./initvenv.sh
source voicebot/bin/activate
pip3 install -r requirements.txt
```

### Configuration

1. Create an environment file for Telegram API credentials:
- Copy the environment template:
```bash
cp.env.template.env.dev
```
- Fill out the `.env.dev` file with your Telegram API data.

### Running the Application

To run TalkyBotty, execute the following commands:

```bash
cd TalkyBotty
source voicebot/bin/activate
python3 main.py
```

This will start the application, allowing it to process incoming voice messages and videos according to its current capabilities.

