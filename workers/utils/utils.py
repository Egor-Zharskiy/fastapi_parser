import bs4.element


def parse_query(query: str):
    params = {}
    try:
        for item in query.split('&'):
            key, value = item.split('=')
            if key in params:
                params[key].append(value)
            else:
                params[key] = [value]

    except ValueError:
        return {"error": "Incorrect format of the query"}
    except Exception as e:
        return {"error": f"An unexpected error occurred {str(e)}"}
    return params


def validate_price(price_tag: bs4.ResultSet):
    for el in price_tag:
        price_text = el.text.strip()
        if 'р.' in price_text:
            return price_text

    return None
