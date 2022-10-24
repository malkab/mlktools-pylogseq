import re

str = "CLOCK: [2022-10-26 Mon 07:54:14]--[2022-10-26 Mon 08:26:28] =>  00:32:14\nCLOCK: [2022-10-27 Mon 07:54:14]--[2022-10-27 Mon 08:26:28] =>  00:32:14"

print(str)

regex = r"(\s?CLOCK:)\s\[(.*)\s(.*)\s(.*)\]--\[(.*)\s(.*)\s(.*)\] =>  (.*)\n"

print(re.findall(regex, str))


# s = """
# Peter (08:16):
# Hi
# What's up?
# ;-D

# Anji Juo (09:13):
# Hey, I'm using WhatsApp!

# Peter (11:17):
# Could you please tell me where is the feedback?

# Anji Juo (19:13):
# I don't know where it is.

# Anji Juo (19:14):
# Do you by any chance know where I can catch a taxi ?
# 🙏🙏🙏
# """

# regex = r"^(?P<user>.*?)\s*\((?P<hhmm>(?:\d|[01]\d|2[0-3]):[0-5]\d)\):\s*(?P<Quote>.*(?:\n(?!\n).*)*)"

# print(re.findall(regex, s, re.M))
