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
