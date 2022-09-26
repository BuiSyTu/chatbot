import re

date_patterns = [
    "(\d{4})-((\d{2})|(\d{1}))-((\d{2})|(\d{1}))",
    "((\d{2})|(\d{1}))-((\d{2})|(\d{1}))-(\d{4})",
    "(\d{4})/((\d{2})|(\d{1}))/((\d{2})|(\d{1}))",
    "((\d{2})|(\d{1}))\/((\d{2})|(\d{1}))\/(\d{4})",
    "((\d{2})|(\d{1})) \/ ((\d{2})|(\d{1})) \/ (\d{4})",
    "((\d{2})|(\d{1}))/((\d{2})|(\d{1}))",
    "((\d{2})|(\d{1})) / ((\d{2})|(\d{1}))",
    "((\d{2})|(\d{1}))-((\d{2})|(\d{1}))",
    "((\d{2})|(\d{1})) - ((\d{2})|(\d{1}))"
]


def check_date(string):
    rs = []
    for pattern in date_patterns:
        matches = re.finditer(pattern, string, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            rs.append(match.group())
    return rs

print(check_date("Ngày 12/11"))
