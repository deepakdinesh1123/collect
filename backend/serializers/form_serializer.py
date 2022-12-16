def serialize_form(form: dict) -> dict:
    for key in form.keys():
        form[key] = str(form[key])
    return form
