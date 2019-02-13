# whatsapp_chat_analyser - python scripts
analyse whatsapp chats between 2 or more people to produce the following info: 

- top 10 words / person
- top 10 emojis / person
- message number / time / person
- number of words used / time / person
- number of emojis used / time / person

the project contains two python 3 scripts that output multiple .csv files 
you can then visualise this data using your preferred tools (excel / google sheets / google data studio etc)

# Prerequisites
python 3
a whatsappchat.txt file that you can export from your phone


# Exporting whatsapp chats
please make sure to export without media

- Android: https://faq.whatsapp.com/en/android/23756533
- iOS: https://faq.whatsapp.com/en/iphone/20888066

# Installing
put the exported whatsapp chat file in the same folder as the scripts
unzip the file chat file and name it chat.txt

run whatsapp_message_analyser.py script and it will produce one .csv file with stats per message:
- word count
- emoji count
- date and time

run whatsapp_top10_words_and_emojis.py script and it will produce one .csv file per person to include:
- top 10 emojis by useage frequency
- top 10 words by useage frequency


# notes
I welcome any feedback / suggestions / requests


