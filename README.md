# Telegram-Messages-Forwarder

This project is a **Telegram message forwarding bot**. It listens for messages from users, groups, and channels in real-time and forwards them to a specified chat.

⭐ **Please leave a star for the project.**  
This project is free and open-source. Your support with a star helps motivate future development! ⭐  

## Setup

To install and set up the project:

```bash
git clone https://github.com/Er-Simon/Telegram-Messages-Forwarder Telegram-Messages-Forwarder
cd Telegram-Messages-Forwarder
pip install -r requirements.txt
```

## How to Use

1. **Create a Telethon Session**:  
   The program will guide you through creating a Telethon session. You will need your `api_id` and `api_hash`, which you can obtain from [my.telegram.org](https://my.telegram.org).
   
2. **Select Source and Destination Chats**:  
   After creating the session, the bot will display all chats your account has access to. You can then specify:
   - A **destination chat** (where messages will be forwarded).  
     **Note**: You must have permission to send messages in the destination chat.
   - One or more **source chats** (from which the bot will listen for messages and forward them).

## Run

To start the bot:

```bash
python3 main.py
```

---

## Supported Features

- **Real-time Message Forwarding**:  
  The bot listens for messages in real-time from the specified source chats (users, groups, or channels) and forwards them to the destination chat.

- **ID-based Tracking**:  
  The bot tracks chats using their unique IDs, ensuring that forwarding continues to work even if chat usernames change.

- **Logging System**:  
  The bot logs all operations, making it easier to track forwarded messages and debug any issues.

---

## Future Releases 🚀

Additional features will be released as the project gains more stars:

- **Publish Messages via Bot in Destination Chat**  
  *Release at 100 stars* ⭐  
  This feature will allow the bot to publish messages in the destination chat using a Telegram bot account, instead of relying on the user's account.

- **Message Filtering System**  
  *Release at 150 stars* ⭐

---

## Contributions & Feedback

The project is still in development. If you find any bugs or have suggestions for improvement, feel free to open an issue. ⚠️

