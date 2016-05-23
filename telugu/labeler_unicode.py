
_all_chars = (u' ఁంఃఅఆఇఈఉఊఋఌఎఏఐఒఓఔ'
             u'కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమ'
             u'యరఱలళవశషసహ'
             u'ఽాిీుూృౄెేైొోౌ్'
             u'ౘౙౠౡౢౣ'
             u'౦౧౨౩౪౫౬౭౮౯')

num_labels = len(_all_chars) + 1


def get_labels(text):
    """
    A basic conversion of unicode telugu text to list of labels (indices)
    Looks each unicode character seperately.
    If not found in all_chars, gives out a 0.
    :param text: str
    :return: list of int
    """
    return [_all_chars.find(char)+1 for char in text]
