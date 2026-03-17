import asyncio
from telethon import TelegramClient
from telethon.tl.types import User, MessageActionContactSignUp

# ====== Configuration ======
API_ID = 12345678
API_HASH = "your_api_hash_here"
SESSION_NAME = "tg_cleanup_session"

DRY_RUN = True  # True = print only, no deletion; False = actually delete
SKIP_BOTS = True
# ===================


def display_name(user: User) -> str:
    return (
        f"{user.first_name or ''} {user.last_name or ''}".strip()
        or user.username
        or str(user.id)
    )


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    checked_dialogs = 0
    matched_joined_only = 0
    matched_deleted_account = 0
    deleted_dialogs = 0

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        # Only process private user chats; skip groups, channels, and self
        if not isinstance(entity, User):
            continue
        if entity.is_self:
            continue
        if SKIP_BOTS and getattr(entity, "bot", False):
            continue

        checked_dialogs += 1
        name = display_name(entity)

        should_delete = False
        reason = None

        # Rule 1: The other user is a deleted account — delete directly
        if getattr(entity, "deleted", False):
            should_delete = True
            reason = "deleted account"
            matched_deleted_account += 1

        else:
            # Rule 2: Only one message, and it is "joined Telegram"
            msgs = []
            async for msg in client.iter_messages(entity, limit=2):
                msgs.append(msg)

            if len(msgs) == 1:
                only_msg = msgs[0]
                if isinstance(getattr(only_msg, "action", None), MessageActionContactSignUp):
                    should_delete = True
                    reason = "single 'joined Telegram' message"
                    matched_joined_only += 1

        if should_delete:
            print(f"[MATCH] {name} | user_id={entity.id} | reason={reason}")

            if not DRY_RUN:
                try:
                    # Only delete the dialog on your side
                    await client.delete_dialog(entity, revoke=False)
                    deleted_dialogs += 1
                    print("  -> deleted")
                except Exception as e:
                    print(f"  -> failed: {e}")

    print("\n===== SUMMARY =====")
    print(f"Checked private dialogs      : {checked_dialogs}")
    print(f"Matched joined-only dialogs  : {matched_joined_only}")
    print(f"Matched deleted-account dialogs : {matched_deleted_account}")
    print(f"Deleted dialogs              : {deleted_dialogs}")
    print(f"Mode                         : {'DRY_RUN' if DRY_RUN else 'EXECUTE'}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
