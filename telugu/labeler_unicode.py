
chars = (u' ఁంఃఅఆఇఈఉఊఋఌఎఏఐఒఓఔ'
         u'కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమ'
         u'యరఱలళవశషసహ'
         u'ఽాిీుూృౄెేైొోౌ్'
         u'ౘౙౠౡౢౣ'
         u'౦౧౨౩౪౫౬౭౮౯')

num_labels = len(chars)

def index(char):
    idx = chars.find(char)
    assert idx >= 0
    return idx

def get_labels(text):
    """
    A basic conversion of unicode telugu text to list of labels (indices)
    Looks each unicode character seperately.
    If not found in all_chars, throws error.
    :param text: str
    :return: list of int
    """
    return [index(char) for char in text]
