from flet import TextField


def display_form_error(field: str, message: str, fields: dict[str, TextField]) -> None:
    if field in fields.keys():
        fields[field].error_text = message
