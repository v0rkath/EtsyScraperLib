import re

def format_sales(sales: str) -> str:
    """
    Remove ` Sales` and `,` from the sales quantity.
    Returns:
        The sales figure with only numeric characters.
    """
    new_string = sales.replace(" Sales", "").replace(",", "")

    return new_string


def format_title(title: str) -> str:
    """
    Remove " - Etsy..." from the title.
    Returns:
        The title of the product not including " - Etsy..."
    """
    to_remove = title.find(" - Etsy")
    
    if to_remove != -1:
        new_string = title[:to_remove]

        return new_string
    else:
        print("String doesn't need formatting.")
        return title
    

def format_description(paragraph: str) -> str:
    """
    Tidy up the description so it is almost a 1:1 representation of what is on the store page and remove prefixed whitespace.
    Return:
        Tidied up description.
    """
    removed_whitespace = paragraph.lstrip()
    insert_newline = removed_whitespace.replace(".  ", ". ")

    pattern = r"(?<=[.!?])(?=[^\d\s])"
    split_sentences = re.split(pattern, insert_newline)
    format_paragraphs = "\n".join(split_sentences)
    
    return format_paragraphs