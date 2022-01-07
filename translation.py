# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from googletrans import Translator


def detect_lang(text: str) -> str:
    '''
    Detects text language input
        - Parameters:
            - text(str): The string which language will be detected
        - Returns :
            - str : String containing language input FR -> FRENCH EN -> ENGLISH
    '''
    if len(text) == 0:
        raise ValueError("Empty text")
    return (Translator().detect(text)).lang


def translate(text: str, lg: str) -> str:
    '''
    Translates text to a given language
        - Parameters:
            - text(str): The string to be translated
            - lg(str): Language which the string will be translated to
        - Returns :
            - str : String translated to language input
    '''
    if len(text) == 0 or len(lg) == 0:
        raise ValueError("Parameter missing")
    return Translator().translate(text, dest=lg).text


def handle_traduction(message: str) -> str:
    '''
    Checks input language message and sends translation
    if message language is French the function
    will translate it to English and vice versa
        - Parameter:
            - text(str): Given string to be translated
        - Returns :
            - str : String translated from input language to the other one
    '''
    lang = detect_lang(message)
    if lang != 'en':
        lang_tr = "en"
    else:
        lang_tr = "fr"
    return translate(str(message), lang_tr)
