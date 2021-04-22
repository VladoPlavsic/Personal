
def string_or_null(*args):
    string = ""
    for arg in args:
        if not arg:
            string += "null, "
        else:
            string += f"'{arg}', "

    return string.strip(", ")