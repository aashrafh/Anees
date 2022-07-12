import html
import re

TASHKEEL = (u'\u064b', u'\u064c', u'\u064d', u'\u064e',
            u'\u064f', u'\u0650', u'\u0652', u'\u0651', u'\u0640')

EMOJIS = r"[^0-9\u0621-\u063A\u0640-\u066C\u0671-\u0674a-zA-Z\[\]!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ»؛\s+«–…‘]"

url_patterns = [
    r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
    r"@(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$@iS",
    r"http[s]?://[a-zA-Z0-9_\-./~\?=%&]+",
    r"www[a-zA-Z0-9_\-?=%&/.~]+",
    r"[a-zA-Z]+\.com",
    r"(?=http)[^\s]+",
    r"(?=www)[^\s]+",
    r"://",
]


def strip_tashkeel(text):
    for char in TASHKEEL:
        text = text.replace(char, "")
    return text


def strip_urls(text):
    for pattern in url_patterns:
        text = re.sub(pattern, " [رابط] ", text)
    return text


def strip_emails(text):
    text = re.sub(r"@[\w\d]+", " [بريد] ", text)
    text = re.sub(r"\S+@\S+", " [بريد] ", text)
    text = re.sub(r"[\w-]+@([\w-]+\.)+[\w-]+", " [بريد] ", text)
    return text


def preprocess(text):
    text = str(text)
    text = html.unescape(text)  # remove html tags
    text = re.sub("<br />", " ", text)  # remove html br tags
    text = re.sub("</?[^>]+>", " ", text)  # remove html tags
    text = strip_tashkeel(text)  # remove tashkeel
    text = strip_urls(text)  # remove urls
    text = strip_emails(text)  # remove emails
    text = text.translate(str.maketrans(
        "٠١٢٣٤٥٦٧٨٩", "0123456789"))  # remove hindi digits
    text = re.compile(r"(\D)\1{2,}", re.DOTALL).sub(
        r"\1\1", text)  # remove repeating characters
    text = re.sub(
        "([^0-9\u0621-\u063A\u0641-\u064A\u0660-\u0669a-zA-Z\[\]])",
        r" \1 ",
        text,
    )  # remove non-arabic characters
    text = re.sub(
        "(\d+)([\u0621-\u063A\u0641-\u064A\u0660-\u066C]+)", r" \1 \2 ", text
    )  # whitespace between words and numbers
    text = re.sub(
        "([\u0621-\u063A\u0641-\u064A\u0660-\u066C]+)(\d+)", r" \1 \2 ", text
    )   # whitespace between words and numbers
    text = text.replace("/", "-")   # replace / with -
    text = re.sub(EMOJIS, " ", text)  # remove emojis
    text = " ".join(text.replace("\uFE0F", "").split())  # remove extra spaces

    return text


def tokenize_arabic_data(tokenizer, prefix, dialect_prefix):
    print(f"Loading the {prefix} utters...")

    dials = []
    with open(f"{DATA_PATH}/{prefix}_utters.json", 'r') as f:
        dials = json.load(f)

    print(f"Tokenize the {prefix} utters...")
    ids = []
    for dial in tqdm(dials):
        dial_ids = []
        for utter in dial:
            proecessed_utter = preprocess(utter)
            # tokens = tokenizer.tokenize(proecessed_utter)
            # token_ids = tokenizer.convert_tokens_to_ids(tokens)
            token_ids = tokenizer.encode(dialect_prefix + proecessed_utter)
            dial_ids.append(token_ids)
        ids.append(dial_ids)

    assert len(ids) == len(dials)
    with open(f"{DATA_PATH}/monsoon_{prefix}_ids.json", 'w') as f:
        json.dump(ids, f, ensure_ascii=False)
    print(f"Saved the {prefix} ids.")
