import os
import psycopg2

from tkinter import Label, Text

from dotenv import load_dotenv
from psycopg2 import DataError, ProgrammingError

load_dotenv()


def get_connection_to_db():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"))
    return conn


def get_cursor_data(query, params=None):
    conn = get_connection_to_db()
    cur = conn.cursor()
    cur.execute(query % params)
    cur_data = cur.fetchone()
    conn.commit()
    conn.close()
    return cur_data


def get_all_words():
    query = f"""SELECT * FROM vocabulary"""
    try:
        conn = get_connection_to_db()
        cur = conn.cursor()
        cur.execute(query)
        words = cur.fetchall()
        vocabulary = []
        for word in words:
            vocabulary.append(word[0])
        return vocabulary
    except(DataError, ProgrammingError):
        return None


def save_new_word(word: str, label=None):
    query = f"""INSERT INTO vocabulary (word)
                VALUES (LOWER('%(word)s'))
                RETURNING word;"""
    vocabulary = get_all_words()
    if word.lower() not in vocabulary:
        try:
            word = get_cursor_data(
                query, {'word': word}
            )
            if label:
                label["text"] = f"New word ({word[0]}) added"
            return word[0]
        except(DataError, ProgrammingError):
            if label:
                label["text"] = "Error occurred"
            return None
    else:
        if label:
            label["text"] = f"The word {word[0].lower()} might be already in vocabulary"
        return None


def delete_word(word: str, label):
    query = f"""DELETE FROM vocabulary
                WHERE word = '%(word)s'"""
    vocabulary = get_all_words()
    if word.lower() in vocabulary:
        try:
            conn = get_connection_to_db()
            cur = conn.cursor()
            cur.execute(query % {'word': word})
            conn.commit()
            label["text"] = f"Word ({word}) was deleted"
            return True
        except(DataError, ProgrammingError):
            label["text"] = "Error occurred"
            return None
    else:
        label["text"] = f"The word {word.lower()} is not in vocabulary yet"
        return None


def add_new_vocabulary(text: str, label):
    vocabulary = text[0:-1].split(", ")
    added_words = []
    for word in vocabulary:
        new_word = save_new_word(word)
        if new_word:
            added_words.append(new_word)
    label["text"] = f"New words added to vocabulary"
    return True


def replace_vocabulary(text: str, label):
    vocabulary = text[0:-1].split(", ")
    query = f"""TRUNCATE vocabulary;
                DELETE FROM vocabulary;"""
    try:
        conn = get_connection_to_db()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        added_words = []
        for word in vocabulary:
            new_word = save_new_word(word)
            if new_word:
                added_words.append(new_word)
        label["text"] = f"All vocabulary words are replaced with new ones"
        return True
    except(DataError, ProgrammingError):
        return False


def get_suitable_for_condition_words(condition: str, check: int, label: Label, text: Text):
    all_words = get_all_words()
    list_of_suitable_words = []

    for word_in_db in all_words:
        comparative_list = []
        for letter in condition:
            if letter.lower() in word_in_db and condition.count(letter.lower()) <= word_in_db.count(letter.lower()):
                comparative_list.append(letter)

        if condition == "".join(comparative_list):
            list_of_suitable_words.append(word_in_db)

    label["text"] = f"condition: {condition}\nsuitable for the condition words: {len(list_of_suitable_words)}"
    text.delete(1.0, "end")
    list_of_suitable_words = sorted(list_of_suitable_words)

    if check == 0:
        n = 10
    elif check == 1:
        n = 50
    else:
        n = len(list_of_suitable_words)

    for el in list_of_suitable_words[:n]:
        text.insert(list_of_suitable_words.index(el)+1.0, f"{str(list_of_suitable_words.index(el) + 1)}. {el} \n")
    return list_of_suitable_words