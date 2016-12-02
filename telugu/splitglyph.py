import re

pattern = re.compile(r'([క-హ]|్[క-హ]|[ా-్])')


def akshara_to_glyphs(akshara):
    if akshara[-1] in "ృౄౢౣ":
        return akshara_to_glyphs(akshara[:-1]) + [akshara[-1]]

    elif len(akshara) <= 2:
        return [akshara]

    elif akshara[1] == "్":
        parts = pattern.findall(akshara)

        if len(akshara) % 2 == 0:
            return [parts[0]+parts[-1]] + parts[1:-1]
        else:
            return parts

    else:
        raise ValueError("Did not understand akshara: ", akshara)