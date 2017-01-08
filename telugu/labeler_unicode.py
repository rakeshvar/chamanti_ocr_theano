
symbols_str = (u' ఁంఃఅఆఇఈఉఊఋఌఎఏఐఒఓఔ'
         u'కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమ'
         u'యరఱలళవశషసహ'
         u'ఽాిీుూృౄెేైొోౌ్'
         u'ౘౙౠౡౢౣ'
         u'౦౧౨౩౪౫౬౭౮౯')

symbols = list(symbols_str)

def get_labels(text):
    """
    A basic conversion of unicode telugu text to list of labels (indices)
    Looks each unicode character separately.
    If not found in all_chars, throws error.
    :param text: str
    :return: list of int
    """
    if type(text) is list:
        text = ''.join(text)

    return [symbols_str.index(char) for char in text]


def get_chars(labels):
    """
    It converts labels to unicode telugu text.
    It is the inverse of get_labels.
    :param labels: list of labels
    :return: list of int
    """
    return [symbols[i] for i in labels]
