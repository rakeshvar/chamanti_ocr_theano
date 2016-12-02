
symbols_str = (u' ఁంఃఅఆఇఈఉఊఋఌఎఏఐఒఓఔ'
         u'కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమ'
         u'యరఱలళవశషసహ'
         u'ఽాిీుూృౄెేైొోౌ్'
         u'ౘౙౠౡౢౣ'
         u'౦౧౨౩౪౫౬౭౮౯')

symbols = [symb for symb in symbols_str]

def get_labels(text):
    """
    A basic conversion of unicode telugu text to list of labels (indices)
    Looks each unicode character seperately.
    If not found in all_chars, throws error.
    :param text: str
    :return: list of int
    """
    if type(text) is list:
        text = ''.join(text)

    return [symbols_str.index(char) for char in text]
