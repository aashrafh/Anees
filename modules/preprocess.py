import re
import string
# transform "ث" to "ت"
arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations

arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
spaces = ' '*len(punctuations_list)

# need to be added to the stemming


def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_punctuations(text):
    translator = str.maketrans(punctuations_list, spaces)
    return text.translate(translator)


def number_change(text):
    hindi_nums = "٠١٢٣٤٥٦٧٨٩"
    arabic_nums = "0123456789"
    hindi_to_arabic_map = str.maketrans(hindi_nums, arabic_nums)
    text = text.translate(hindi_to_arabic_map)
    return text


def pre_process(text):
    text = remove_punctuations(text)
    text = remove_diacritics(text)
    text = normalize_arabic(text)
    text = number_change(text)
    return text
