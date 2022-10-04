#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check_brackets(text, brackets):
    # {brackets[i]: brackets[i+1] for i in range(0, len(brackets)-1, 2)}
    associative_dict = dict(zip(brackets[0::2], brackets[1::2]))  # opening brackets
    # closing_dict = dict(zip(brackets[1::2], brackets[0::2]))

    closing_brackets = []
    for c in text:
        if c in brackets:
            if c in associative_dict:  # Si ouvrant
                closing_brackets.append(associative_dict[c])
            elif len(closing_brackets) != 0 and c != closing_brackets.pop():
                # Si fermant et non dans le haut de la pile
                return False
            """elif c == closing_brackets[-1]:  # Si fermant et est dans le haut de la pile
                closing_brackets.pop(-1)
            else:  # Fermant et non dans la pile
                return False"""

    return len(closing_brackets) == 0  # Il n'y a plus de brackets


def remove_comments(full_text, comment_start, comment_end):
    text = full_text
    next_start = 0
    while True:
        start = text.find(comment_start, next_start)
        end = text.find(comment_end, next_start)

        if start == -1 and end == -1:
            return text  # On a enlevé tout les commentaires

        if end < start or (start == -1) != (end == 1):
            return None  # Mauvais String

        text = text[:start] + text[end + len(comment_end):]
        next_start = start


def get_tag_prefix(text, opening_tags, closing_tags):
    for otag, ctag in zip(opening_tags, closing_tags):
        if text.startswith(otag):
            return otag, None
        elif text.startswith(ctag):
            return None, ctag,
    return None, None


def check_tags(full_text, tag_names, comment_tags):
    text = remove_comments(full_text, *comment_tags)

    if text is None:
        return False  # Protection aginst bad comments

    tags_dict = {f"<{name}>": f"</{name}>" for name in tag_names}
    tag_stack = []
    while len(text) != 0:
        text = text.lstrip()
        opening, closing = get_tag_prefix(text, tags_dict.keys(), tags_dict.values())

        if opening is not None:
            tag_stack.append(tags_dict[opening])
            text = text[len(opening):]

        elif closing is not None:
            if len(tag_stack) != 0 and closing != tag_stack.pop():
                return False
            text = text[len(closing):]
        else:
            next_tag = text.find("<", 1)
            if next_tag != -1:
                text = text[next_tag:]
    return len(tag_stack) == 0



if __name__ == "__main__":
    brackets = ("(", ")", "{", "}", "[", "]")
    yeet = "(yeet){yeet}"
    yeeet = "({yeet})"
    yeeeet = "({yeet)}"
    yeeeeet = "(yeet"
    print(check_brackets(yeet, brackets))
    print(check_brackets(yeeet, brackets))
    print(check_brackets(yeeeet, brackets))
    print(check_brackets(yeeeeet, brackets))
    print()

    spam = "Hello, world!"
    eggs = "Hello, /* OOGAH BOOGAH world!"
    parrot = "Hello, OOGAH BOOGAH*/ world!"
    dead_parrot = "Hello, /*oh brave new */world!"
    print(remove_comments(spam, "/*", "*/"))
    print(remove_comments(eggs, "/*", "*/"))
    print(remove_comments(parrot, "/*", "*/"))
    print(remove_comments(dead_parrot, "/*", "*/"))
    print()

    otags = ("<head>", "<body>", "<h1>")
    ctags = ("</head>", "</body>", "</h1>")
    print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("</h1></body>", otags, ctags))
    print(get_tag_prefix("</body>", otags, ctags))
    print()

    spam = (
        "<html>"
        "  <head>"
        "    <title>"
        "      <!-- Ici j'ai écrit qqch -->"
        "      Example"
        "    </title>"
        "  </head>"
        "  <body>"
        "    <h1>Hello, world</h1>"
        "    <!-- Les tags vides sont ignorés -->"
        "    <br>"
        "    <h1/>"
        "  </body>"
        "</html>"
    )
    eggs = (
        "<html>"
        "  <head>"
        "    <title>"
        "      <!-- Ici j'ai écrit qqch -->"
        "      Example"
        "    <!-- Il manque un end tag"
        "    </title>-->"
        "  </head>"
        "</html>"
    )
    parrot = (
        "<html>"
        "  <head>"
        "    <title>"
        "      Commentaire mal formé -->"
        "      Example"
        "    </title>"
        "  </head>"
        "</html>"
    )
    tags = ("html", "head", "title", "body", "h1")
    comment_tags = ("<!--", "-->")
    print(check_tags(spam, tags, comment_tags))
    print(check_tags(eggs, tags, comment_tags))
    print(check_tags(parrot, tags, comment_tags))
    print()
