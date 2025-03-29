
# import msal
# import requests
# import os
# import sys
# import subprocess
# from datetime import datetime, timedelta
# from dateutil.parser import parse as parse_datetime
# from pytz import timezone
# from msal import PublicClientApplication, SerializableTokenCache

# # === CONFIG ===
# TENANT_ID = "050ea3de-6ab5-4bb6-ae57-0100b14df04d"
# CLIENT_ID = "75f010e1-4873-4b3e-a83a-222c9758a7b8"

# ALERT_IF_IN_NEXT_MINUTES = 10
# ALERT_POPUP_BEFORE_SECONDS = 10

# # === ICONS ===
# NERD_ICON = "󰤙"
# EMOJI_ICON = "📆"
# FREE_ICON = "󱁕"
# FREE_EMOJI = "✅"

# def supports_nerd_fonts():
#     try:
#         return sys.stdout.encoding.lower().startswith("utf")
#     except:
#         return False

# ICON = NERD_ICON if supports_nerd_fonts() else EMOJI_ICON
# FREE = FREE_ICON if supports_nerd_fonts() else FREE_EMOJI

# # === Persistent Token Cache ===
# CACHE_PATH = os.path.expanduser("~/.cache/ms_token.json")
# os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
# cache = SerializableTokenCache()

# if os.path.exists(CACHE_PATH):
#     with open(CACHE_PATH, "r") as f:
#         cache.deserialize(f.read())

# app = PublicClientApplication(
#     client_id=CLIENT_ID,
#     authority=f"https://login.microsoftonline.com/{TENANT_ID}",
#     token_cache=cache
# )

# accounts = app.get_accounts()
# result = app.acquire_token_silent(["Calendars.Read", "Mail.Read"], account=accounts[0]) if accounts else None

# if not result:
#     flow = app.initiate_device_flow(scopes=["Calendars.Read", "Mail.Read"])
#     if "user_code" not in flow:
#         print("❌ Failed to initiate device code flow.")
#         exit(1)
#     print(flow["message"])
#     result = app.acquire_token_by_device_flow(flow)

# if "access_token" not in result:
#     print("❌ Failed to acquire token.")
#     exit(1)

# if cache.has_state_changed:
#     with open(CACHE_PATH, "w") as f:
#         f.write(cache.serialize())

# access_token = result["access_token"]

# # === Calendar Query ===
# start = datetime.utcnow().isoformat() + "Z"
# end = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"

# url = (
#     f"https://graph.microsoft.com/v1.0/me/calendar/calendarView"
#     f"?startDateTime={start}&endDateTime={end}&$orderby=start/dateTime&$top=1"
# )

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Prefer": 'outlook.timezone="America/New_York"',
#     "Content-Type": "application/json"
# }

# response = requests.get(url, headers=headers)
# if response.status_code != 200:
#     print(f"❌ Error: {response.status_code}")
#     exit(1)

# events = response.json().get("value", [])
# if not events:
#     print(f"{FREE} Free")
#     exit(0)

# event = events[0]
# subject = event["subject"]
# start_time = event["start"]["dateTime"]

# EST = timezone("America/New_York")
# start_dt = parse_datetime(start_time)
# if start_dt.tzinfo is None:
#     start_dt = EST.localize(start_dt)

# start_local_str = start_dt.strftime("%I:%M %p")
# now_est = datetime.now(EST)
# minutes_left = int((start_dt - now_est).total_seconds() / 60)

# # === Format time until ===
# # if minutes_left >= 60:
# #     hours = minutes_left // 60
# #     mins = minutes_left % 60
# #     time_until = f"{hours} h {mins} min"
# # else:
# #     time_until = f"{minutes_left} min"

# highlight = False

# if minutes_left >= 60:
#     hours = minutes_left // 60
#     mins = minutes_left % 60
#     time_until = f"{hours} h {mins} min"
# else:
#     time_until = f"{minutes_left} min"
#     highlight = True  # Less than 1 hour

# BLINK_ICON = "󰤙"
# STATIC_ICON = ICON

# if minutes_left <= 10:
#     ICON = "#[blink]" + BLINK_ICON + "#[noblink]"
# elif highlight:
#     ICON = "#[fg=brightmagenta]" + STATIC_ICON + "#[default]"

# # === Tmux popup if meeting is soon ===
# if 0 < minutes_left < ALERT_IF_IN_NEXT_MINUTES:
#     seconds_left = int((start_dt - now_est).total_seconds())
#     if ALERT_POPUP_BEFORE_SECONDS <= seconds_left <= ALERT_POPUP_BEFORE_SECONDS + 10:
#         try:
#             subprocess.run([
#                 "tmux", "display-popup",
#                 "-w", "60%",
#                 "-h", "60%",
#                 "-T", "Upcoming Meeting",
#                 "echo", f"{subject} at {start_local_str} EST"
#             ])
#         except Exception as e:
#             print(f"⚠️ Failed to show tmux popup: {e}")

# # === Get unread email count ===
# mail_url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox?$select=unreadItemCount"
# mail_response = requests.get(mail_url, headers={"Authorization": f"Bearer {access_token}"})
# unread_count = "?"

# if mail_response.status_code == 200:
#     unread_count = mail_response.json().get("unreadItemCount", 0)

# # 📬 Get subject of most recent unread email
# # email_subject = ""
# # mail_url = "https://graph.microsoft.com/v1.0/me/messages?$filter=isRead eq false&$top=1&$select=subject"

# # msg_response = requests.get(mail_url, headers={"Authorization": f"Bearer {access_token}"})
# # if msg_response.status_code == 200:
# #     messages = msg_response.json().get("value", [])
# #     if messages:
# #         raw_subject = messages[0].get("subject", "").strip()
# #         # Truncate and clean it
# #         if len(raw_subject) > 40:
# #             raw_subject = raw_subject[:37] + "..."
# #         email_subject = f"“{raw_subject}”"
# # 📬 Get subject of most recent unread email (first word only)
# email_subject = ""
# msg_response = requests.get(
#     "https://graph.microsoft.com/v1.0/me/messages?$filter=isRead eq false&$top=1&$select=subject",
#     headers={"Authorization": f"Bearer {access_token}"}
# )

# if msg_response.status_code == 200:
#     messages = msg_response.json().get("value", [])
#     if messages:
#         raw_subject = messages[0].get("subject", "").strip()
#         first_word = raw_subject.split(" ")[0] if raw_subject else ""
#         email_subject = f"“{first_word}…”" if first_word else ""


# # === Final tmux status output ===
# # print(f"{ICON} {start_local_str} {subject} ({time_until})   📥 {unread_count}")
# output = f"{ICON} {start_local_str} {subject} ({time_until})"

# if unread_count and unread_count != "0":
#     output += f"   📥 {unread_count}"
#     if email_subject:
#         output += f" {email_subject}"

# print(output)

####################################################
####################################################
####################################################

# import msal
# import requests
# import os
# import sys
# import subprocess
# from datetime import datetime, timedelta
# from dateutil.parser import parse as parse_datetime
# from pytz import timezone
# from msal import PublicClientApplication, SerializableTokenCache

# # === CONFIG ===
# TENANT_ID = "050ea3de-6ab5-4bb6-ae57-0100b14df04d"
# CLIENT_ID = "75f010e1-4873-4b3e-a83a-222c9758a7b8"

# ALERT_IF_IN_NEXT_MINUTES = 10
# ALERT_POPUP_BEFORE_SECONDS = 10

# # === ICONS ===
# NERD_ICON = "󰤙"
# EMOJI_ICON = "📆"
# FREE_ICON = "󱁕"
# FREE_EMOJI = "✅"

# def supports_nerd_fonts():
#     try:
#         return sys.stdout.encoding.lower().startswith("utf")
#     except:
#         return False

# ICON = NERD_ICON if supports_nerd_fonts() else EMOJI_ICON
# FREE = FREE_ICON if supports_nerd_fonts() else FREE_EMOJI

# # === Persistent Token Cache ===
# CACHE_PATH = os.path.expanduser("~/.cache/ms_token.json")
# os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
# cache = SerializableTokenCache()

# if os.path.exists(CACHE_PATH):
#     with open(CACHE_PATH, "r") as f:
#         cache.deserialize(f.read())

# app = PublicClientApplication(
#     client_id=CLIENT_ID,
#     authority=f"https://login.microsoftonline.com/{TENANT_ID}",
#     token_cache=cache
# )

# accounts = app.get_accounts()
# result = app.acquire_token_silent(["Calendars.Read", "Mail.Read"], account=accounts[0]) if accounts else None

# if not result:
#     flow = app.initiate_device_flow(scopes=["Calendars.Read", "Mail.Read"])
#     if "user_code" not in flow:
#         print("❌ Failed to initiate device code flow.")
#         exit(1)
#     print(flow["message"])
#     result = app.acquire_token_by_device_flow(flow)

# if "access_token" not in result:
#     print("❌ Failed to acquire token.")
#     exit(1)

# if cache.has_state_changed:
#     with open(CACHE_PATH, "w") as f:
#         f.write(cache.serialize())

# access_token = result["access_token"]

# # === Calendar Query ===
# start = datetime.utcnow().isoformat() + "Z"
# end = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"

# url = (
#     f"https://graph.microsoft.com/v1.0/me/calendar/calendarView"
#     f"?startDateTime={start}&endDateTime={end}&$orderby=start/dateTime&$top=1"
# )

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Prefer": 'outlook.timezone="America/New_York"',
#     "Content-Type": "application/json"
# }

# response = requests.get(url, headers=headers)
# if response.status_code != 200:
#     print(f"❌ Error: {response.status_code}")
#     exit(1)

# events = response.json().get("value", [])
# if not events:
#     print(f"{FREE} Free")
#     exit(0)

# event = events[0]
# subject = event["subject"]
# start_time = event["start"]["dateTime"]

# EST = timezone("America/New_York")
# start_dt = parse_datetime(start_time)
# if start_dt.tzinfo is None:
#     start_dt = EST.localize(start_dt)

# start_local_str = start_dt.strftime("%I:%M %p")
# now_est = datetime.now(EST)
# minutes_left = int((start_dt - now_est).total_seconds() / 60)

# # === Format time until and determine highlight flag ===
# highlight = False

# if minutes_left >= 60:
#     hours = minutes_left // 60
#     mins = minutes_left % 60
#     time_until = f"{hours} h {mins} min"
# else:
#     time_until = f"{minutes_left} min"
#     highlight = True  # Less than 1 hour

# # === Set icon formatting based on time left ===
# if minutes_left <= 15:
#     formatted_icon = f"#[blink]{ICON}#[noblink]"
# else:
#     formatted_icon = ICON

# # === Tmux popup if meeting is soon ===
# if 0 < minutes_left < ALERT_IF_IN_NEXT_MINUTES:
#     seconds_left = int((start_dt - now_est).total_seconds())
#     if ALERT_POPUP_BEFORE_SECONDS <= seconds_left <= ALERT_POPUP_BEFORE_SECONDS + 10:
#         try:
#             subprocess.run([
#                 "tmux", "display-popup",
#                 "-w", "60%",
#                 "-h", "60%",
#                 "-T", "Upcoming Meeting",
#                 "echo", f"{subject} at {start_local_str} EST"
#             ])
#         except Exception as e:
#             print(f"⚠️ Failed to show tmux popup: {e}")

# # === Get unread email count ===
# mail_url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox?$select=unreadItemCount"
# mail_response = requests.get(mail_url, headers={"Authorization": f"Bearer {access_token}"})
# unread_count = "?"

# if mail_response.status_code == 200:
#     unread_count = mail_response.json().get("unreadItemCount", 0)

# # 📬 Get subject of most recent unread email (first word only)
# email_subject = ""
# msg_response = requests.get(
#     "https://graph.microsoft.com/v1.0/me/messages?$filter=isRead eq false&$top=1&$select=subject",
#     headers={"Authorization": f"Bearer {access_token}"}
# )

# if msg_response.status_code == 200:
#     messages = msg_response.json().get("value", [])
#     if messages:
#         raw_subject = messages[0].get("subject", "").strip()
#         first_word = raw_subject.split(" ")[0] if raw_subject else ""
#         email_subject = f"“{first_word}…”" if first_word else ""

# # === Final tmux status output ===
# output = f"{formatted_icon} {start_local_str} {subject} ({time_until})"

# if unread_count and unread_count != "0":
#     output += f"   📥 {unread_count}"
#     if email_subject:
#         output += f" {email_subject}"

# # If meeting is less than 1 hour away, make the entire output red
# if highlight:
#     output = f"#[fg=red]{output}#[default]"

# print(output)



##############################################

import msal
import requests
import os
import sys
import subprocess
import tempfile
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_datetime
from pytz import timezone
from msal import PublicClientApplication, SerializableTokenCache

# === CONFIG ===
TENANT_ID = "050ea3de-6ab5-4bb6-ae57-0100b14df04d"
CLIENT_ID = "75f010e1-4873-4b3e-a83a-222c9758a7b8"

# 

#############################################

ALERT_IF_IN_NEXT_MINUTES = 10
ALERT_POPUP_BEFORE_SECONDS = 10

# === ICONS ===
NERD_ICON = "󰤙"
EMOJI_ICON = "📆"
FREE_ICON = "󱁕"
FREE_EMOJI = "✅"

def supports_nerd_fonts():
    try:
        return sys.stdout.encoding.lower().startswith("utf")
    except:
        return False

ICON = NERD_ICON if supports_nerd_fonts() else EMOJI_ICON
FREE = FREE_ICON if supports_nerd_fonts() else FREE_EMOJI

def truncate_text(text, max_len):
    """Return text truncated to max_len, appending '...' if truncated."""
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text

# === Persistent Token Cache ===
CACHE_PATH = os.path.expanduser("~/.cache/ms_token.json")
os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
cache = SerializableTokenCache()

if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "r") as f:
        cache.deserialize(f.read())

app = PublicClientApplication(
    client_id=CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    token_cache=cache
)

accounts = app.get_accounts()
result = app.acquire_token_silent(["Calendars.Read", "Mail.Read"], account=accounts[0]) if accounts else None

if not result:
    flow = app.initiate_device_flow(scopes=["Calendars.Read", "Mail.Read"])
    if "user_code" not in flow:
        print("❌ Failed to initiate device code flow.")
        exit(1)
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)

if "access_token" not in result:
    print("❌ Failed to acquire token.")
    exit(1)

if cache.has_state_changed:
    with open(CACHE_PATH, "w") as f:
        f.write(cache.serialize())

access_token = result["access_token"]

# === Calendar Query ===
start = datetime.utcnow().isoformat() + "Z"
end = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"

url = (
    f"https://graph.microsoft.com/v1.0/me/calendar/calendarView"
    f"?startDateTime={start}&endDateTime={end}"
    f"&$orderby=start/dateTime&$top=1"
    f"&$select=subject,start,end,bodyPreview,webLink,attendees"
)

headers = {
    "Authorization": f"Bearer {access_token}",
    "Prefer": 'outlook.timezone="America/New_York"',
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    exit(1)

events = response.json().get("value", [])
meeting_info = None
highlight = False

if events:
    event = events[0]
    subject = event["subject"]
    start_time = event["start"]["dateTime"]
    end_time = event["end"]["dateTime"]

    EST = timezone("America/New_York")
    start_dt = parse_datetime(start_time)
    if start_dt.tzinfo is None:
        start_dt = EST.localize(start_dt)
    end_dt = parse_datetime(end_time)
    if end_dt.tzinfo is None:
        end_dt = EST.localize(end_dt)

    start_local_str = start_dt.strftime("%I:%M %p")
    now_est = datetime.now(EST)
    minutes_left = int((start_dt - now_est).total_seconds() / 60)

    # Format time until and determine highlight
    if minutes_left >= 60:
        hours = minutes_left // 60
        mins = minutes_left % 60
        time_until = f"{hours} h {mins} min"
    else:
        time_until = f"{minutes_left} min"
        highlight = True  # Less than 1 hour

    # Set meeting icon formatting based on time left
    if minutes_left <= 15:
        formatted_icon = f"#[blink]{ICON}#[noblink]"
    else:
        formatted_icon = ICON

    meeting_info = f"{formatted_icon} {start_local_str} {subject} ({time_until})"

    # Tmux popup if meeting is soon
    if 0 < minutes_left < ALERT_IF_IN_NEXT_MINUTES:
        seconds_left = int((start_dt - now_est).total_seconds())
        if ALERT_POPUP_BEFORE_SECONDS <= seconds_left <= ALERT_POPUP_BEFORE_SECONDS + 10:
            detailed_message = (
                f"Subject: {subject}\n"
                f"Start: {start_local_str} EST\n"
                f"End: {end_dt.strftime('%I:%M %p')} EST\n"
            )
            if event.get("bodyPreview"):
                detailed_message += f"Notes: {event['bodyPreview']}\n"
            if event.get("webLink"):
                detailed_message += f"URL: {event['webLink']}\n"
            if event.get("attendees"):
                attendees_list = []
                for attendee in event["attendees"]:
                    email_info = attendee.get("emailAddress", {})
                    name = email_info.get("name", "Unknown")
                    address = email_info.get("address", "")
                    attendees_list.append(f"{name} <{address}>")
                detailed_message += f"Attendees: {', '.join(attendees_list)}\n"

            try:
                with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
                    tmp.write(detailed_message)
                    tmp_filename = tmp.name
                subprocess.run([
                    "tmux", "display-popup",
                    "-S", "fg=#eba0ac",
                    "-w", "50%",
                    "-h", "50%",
                    "-d", "#{pane_current_path}",
                    "-T", "Meeting Details",
                    "bash", "-c", f"cat {tmp_filename}; rm {tmp_filename}"
                ])
            except Exception as e:
                print(f"⚠️ Failed to show tmux popup: {e}")

# === Get unread email count ===
mail_url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox?$select=unreadItemCount"
mail_response = requests.get(mail_url, headers={"Authorization": f"Bearer {access_token}"})
if mail_response.status_code == 200:
    unread_count = mail_response.json().get("unreadItemCount", 0)
else:
    unread_count = 0

# === Get details of the most recent unread email ===
msg_url = (
    "https://graph.microsoft.com/v1.0/me/messages?"
    "$filter=isRead eq false"
    "&$top=1"
    "&$select=subject,bodyPreview,from"
)
msg_response = requests.get(msg_url, headers={"Authorization": f"Bearer {access_token}"})

detailed_email_info = ""
if msg_response.status_code == 200:
    messages = msg_response.json().get("value", [])
    if messages:
        msg0 = messages[0]
        full_subject = msg0.get("subject", "").strip()
        body_preview = msg0.get("bodyPreview", "").strip()
        from_obj = msg0.get("from", {}).get("emailAddress", {})
        from_name = from_obj.get("name", "")
        
        # Build a combined string like "FromName: Subject [BodySnippet]"
        combined = f"{from_name}: {full_subject} [{body_preview}]"
        detailed_email_info = combined

# Decide how much to truncate based on whether we have a meeting or not
if meeting_info:
    # If there's a meeting, use a shorter length
    max_len_for_email = 15
else:
    # If no meeting, show a bit more detail
    max_len_for_email = 25

# Truncate the combined email info
detailed_email_info = truncate_text(detailed_email_info, max_len_for_email)

# Blink the email icon if there are any unread messages
if unread_count > 0:
    email_icon = "#[blink]📥#[noblink]"
else:
    email_icon = "📥"

# Final email status
if unread_count > 0 and detailed_email_info:
    email_status = f"{email_icon} {unread_count} {detailed_email_info}"
else:
    # If no unread messages or no extra info, just show the count
    email_status = f"{email_icon} {unread_count}"

# === Final tmux status output ===
if meeting_info:
    # If highlight is True (<1 hour), color the meeting info red, then reset
    if highlight:
        meeting_info = f"#[fg=red]{meeting_info}#[default]"
    output = meeting_info
else:
    output = f"{FREE} Free"

# Append email info in a different color
output += f" #[fg=cyan]{email_status}#[default]"

print(output)