import re
from collections import Counter
import emoji as e
import emoji.unicode_codes as emoji_unicode_dict
import csv


# Replace "chat.txt" with your chat filename below
whatsapp_chat = 'chat.txt'


def import_file(filename):  # import txt file, cleanup and produce a list of messages
    file = open(filename, encoding="utf8")
    lines = []
    for line in file:
        line = re.sub(r'image omitted', '', line)
        line = re.sub(r'\u200eimage', '', line)
        line = re.sub(r'video omitted', '', line)
        line = re.sub(r'\u200e', '', line)
        if re.findall(r"\[(\d{2}/\d{2}/\d{4})", line):
            lines.append(line.strip())
        else:
            last_line = lines.pop()
            line = last_line.strip() + " " + line.strip()
            lines.append(line)
    return lines


def extract_name(line):
    name = re.findall(r".*?:.*?\]\s(.*?):", line)
    return str(name[0])


def extract_message(line):
    message = re.findall(r"\[\d{2}/\d{2}/\d{4}.*?:.*?\]\s.*?:(.*)", line)
    message = str(message[0]).strip()
    return message


def stop_word_filter(stop_words_file, text):
    file = open(stop_words_file)
    stop_words_list = file.read().split()
    if text in stop_words_list:
        return ''
    else:
        return text


def remove_special_charachters(text):
    text = re.sub(r"\W", '', text)
    return text


def strip_emoji(text):
    no_emoji_text = ''
    for charachter in text:
        if charachter not in emoji_unicode_dict.UNICODE_EMOJI:
            no_emoji_text = no_emoji_text + charachter
    return no_emoji_text


def extract_emoji(text):
    output_list = []
    emojis = e.emoji_lis(text)
    for emoji in emojis:
            emoji = emoji['emoji']
            output_list.append(emoji)
    return output_list


def extract_emoji_from_words_list(words_list):
    emoji_output_list = []
    for word in words_list:
        for emoji in extract_emoji(word):
            emoji_output_list.append(emoji)
    return emoji_output_list


def extract_words_from_line(line):  # make a list of all words
    all_words = []
    message = extract_message(line)
    words = message.split()
    for word in words:
        all_words.append(word)
    return all_words


def cleanup_word_list(words_list):
    words_output_list = []  # strip emoji and stop words and make a clean list of all words
    for word in words_list:
        word = strip_emoji(word)
        word = word.lower()
        word = remove_special_charachters(word)
        word = stop_word_filter('stop_words.txt', word)

        if len(word) > 0:
            words_output_list.append(word)
        else:
            continue
    return words_output_list


def extract_all_names(lines):
    names = []
    for line in lines:
        name = extract_name(line)
        if name not in names:
            names.append(name)
    return names


def build_names_words_dictionary(lines):
    names_words_dictionary = {}
    for line in lines:
        name = extract_name(line)
        if name not in names_words_dictionary:
            names_words_dictionary[name] = None
        words = extract_words_from_line(line)
        if not names_words_dictionary.get(name):
            names_words_dictionary.update({name: words})
        else:
            current_words = names_words_dictionary.get(name)
            new_words = current_words + words
            names_words_dictionary.update({name: new_words})
    return names_words_dictionary


lines = import_file(whatsapp_chat)
names_words_dictionary = build_names_words_dictionary(lines)

for name in names_words_dictionary:
    all_words = names_words_dictionary[name]
    words_output_list = cleanup_word_list(all_words)

    # most_common() produces k frequently encountered input values and their respective counts.
    word_counter = Counter(words_output_list)
    most_occur_words = word_counter.most_common()
    top_words = most_occur_words[0:10]

    top_words_filename = 'top_words' + '_' + name + ".csv"
    with open(top_words_filename, mode='w') as top_words_csv_file:
        fieldnames = ['name', 'top_word', 'frequency']
        writer = csv.DictWriter(top_words_csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for word in top_words:
            result = {'name': name,
                      'top_word': word[0],
                      'frequency': word[1]}
            writer.writerow(result)
    top_words_csv_file.close()

    emoji_output_list = extract_emoji_from_words_list(all_words)
    emoji_counter = Counter(emoji_output_list)
    most_occur_emojis = emoji_counter.most_common()
    top_emojis = most_occur_emojis[0:10]

    top_emoji_filename = 'top_emoji' + '_' + name + ".csv"
    with open(top_emoji_filename, mode='w') as top_emojis_csv_file:
        fieldnames = ['name', 'top_emoji', 'frequency']
        writer = csv.DictWriter(top_emojis_csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for emoji in top_emojis:
            result = {'name': name,
                      'top_emoji': emoji[0],
                      'frequency': emoji[1]}
            writer.writerow(result)
    top_emojis_csv_file.close()

