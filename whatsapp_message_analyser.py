import re
import csv
import emoji as e
from emoji.unicode_codes import UNICODE_EMOJI


# Replace "chat.txt" with your chat filename below
whatsapp_chat = 'chat.txt'


def build_line(date, hour, name, message, word_count, emoji_count, message_count):
    return {
        "date": date,
        "hour": hour,
        "name": name,
        "message": message,
        "word_count": word_count,
        "emoji_count": emoji_count,
        "message_count": message_count
    }


def import_file(filename):  # import txt file, cleanup and produce a list of lines that contain all message info
    file = open(filename, encoding="utf8")
    lines = []

    for line in file:
        line = re.sub(r'--image omitted', '', line)
        line = re.sub(r'--video omitted', '', line)
        line = re.sub(r'--audio omitted', '', line)
        line = re.sub(r'\u200e', '', line)
        if re.findall(r"\[(\d{2}/\d{2}/\d{4})", line):
            lines.append(line.strip())
        else:
            last_line = lines.pop()
            line = last_line.strip() + " " + line.strip()
            lines.append(line)
    return lines


def extract_date(line):
    date = re.findall(r"\[(\d{2})/(\d{2})/(\d{4})", line)
    YYYYMMDD = str(date[0][2]) + str(date[0][1]) + str(date[0][0])
    return YYYYMMDD


def extract_hour(line):
    hour = re.findall("\[\d{2}/\d{2}/\d{4},.(\d{2}):\d{2}:\d{2}\]", line)
    return str(hour[0])


def extract_name(line):
    name = re.findall(r".*?:.*?\]\s(.*?):", line)
    return str(name[0])


def extract_message(line):
    message = re.findall(r"\[\d{2}/\d{2}/\d{4}.*?:.*?\]\s.*?:(.*)", line)
    message = str(message[0]).strip()
    return message


def strip_emoji(text):
    no_emoji_text = ''
    for character in text:
        if character not in UNICODE_EMOJI:
            no_emoji_text = no_emoji_text + character
    return no_emoji_text


def export_all_lines_csv(input_txt_file, export_filename):

    file = import_file(input_txt_file)
    results = []
    for line in file:
        full_message = extract_message(line)
        emoji_count = e.emoji_count(full_message)
        emojiless_message = strip_emoji(full_message)
        if len(emojiless_message) > 0:
            word_count = len(emojiless_message.split())
        else:
            word_count = 0
        results.append(build_line(extract_date(line), extract_hour(line), extract_name(line), full_message, word_count, emoji_count, 1))
    fields_to_write_to_csv = ["date", "hour", "name", "message", "word_count", "emoji_count", "message_count"]
    with open(export_filename, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields_to_write_to_csv)

        writer.writeheader()
        for line in results:
            writer.writerow(line)


export_all_lines_csv(whatsapp_chat, 'parsed_chat_output.csv')
