# Telegram Dialog Cleanup Script

A small Python script to automatically clean up unnecessary Telegram dialogs.

This tool connects to your Telegram account using the official MTProto API (via Telethon) and removes dialogs that are typically useless clutter, such as:

- Conversations that contain only the message "xxx joined Telegram"
- Conversations with deleted accounts

The script is designed to help reduce noise in long-time Telegram accounts that have accumulated many empty or inactive chats.

---

## Features

The script scans all private dialogs in your Telegram account and deletes dialogs that match the following rules.

### 1. Empty "Joined Telegram" dialogs

Delete a dialog if:

- The dialog contains exactly one message
- That message is a system message:
  `"<contact> joined Telegram"`

These dialogs typically appear when a phone contact creates a Telegram account but you never actually chatted.

---

### 2. Deleted accounts

Delete a dialog if:

- The other account is marked by Telegram as **Deleted Account**

These are usually abandoned accounts that no longer exist.

---

## Safety

The script includes a **dry-run mode**.

When enabled, the script:

- scans dialogs
- prints which dialogs would be deleted
- **does not delete anything**

You should run dry-run first to verify the results.

---

## Requirements

Python 3.8+

Install dependency:

```
pip install telethon
```

---

## Telegram API Credentials

You must obtain your own Telegram API credentials.

1. Go to: https://my.telegram.org
2. Log in with your phone number
3. Open: **API Development Tools**
4. Create an application

You will receive:

- `API_ID`
- `API_HASH`

Insert these values into the script.

Example:

```python
API_ID = 12345678
API_HASH = "your_api_hash_here"
```

---

## Usage

### Step 1 — Run in preview mode

Make sure the script contains:

```python
DRY_RUN = True
```

Then run:

```
python tg_cleanup.py
```

The script will print dialogs that match the cleanup rules.

Example output:

```
[MATCH] John Doe | user_id=123456789 | reason=single 'joined Telegram' message
[MATCH] Deleted Account | user_id=987654321 | reason=deleted account
```

Nothing will be deleted.

---

### Step 2 — Execute deletion

After verifying the output, change:

```python
DRY_RUN = False
```

Run the script again.

Matched dialogs will be removed from your Telegram account.

---

## What Exactly Gets Deleted

The script deletes the entire dialog from **your side only**.

This means:

- The conversation disappears from your chat list
- The other user is not affected
- No messages are deleted from the other user's account

---

## What the Script Does NOT Touch

The script intentionally ignores:

- group chats
- channels
- bots
- saved messages
- any dialog containing real conversations

Only the two conditions described above are processed.

---

## Example Use Case

Accounts that have been used for many years often accumulate hundreds of dialogs like:

```
Alice joined Telegram
Bob joined Telegram
Charlie joined Telegram
```

These dialogs contain no conversation and only clutter the chat list.

This script removes them automatically.

---

## Notes

- First run requires Telegram login via SMS code.
- A session file will be created locally so you do not need to log in again.
- The script uses Telegram's official MTProto client API through Telethon.
