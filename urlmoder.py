
def mod_url(url:str, template: str, data: int):
    tmp = template.replace('=', f"={str(data)}")
    new_tmp = ""

    for char in template:
        if char == '=':
            new_tmp += tmp

    url = url.replace(template, new_tmp)

    return url
            