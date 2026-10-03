"""Scope: Validate and normalize quote preferences shared by both upload transports."""


class QuotePreferences:
    def __init__(self, body: dict) -> None:
        if not isinstance(body, dict):
            raise ValueError("The quote request must be an object.")
        selected = body.get("selected")
        if not isinstance(selected, dict) or set(selected) != {"machining", "painting", "installation"}:
            raise ValueError("Choose the services for your request.")
        if any(type(value) is not bool for value in selected.values()) or not selected["machining"]:
            raise ValueError("This submission sends CNC machining requests only.")
        self.values = {"selected": selected}
        for name, maximum in {"title": 200, "finish": 20, "colour": 200, "postcode": 20,
                              "timing": 30, "notes": 2000}.items():
            value = body.get(name, "")
            if not isinstance(value, str) or len(value) > maximum:
                raise ValueError(f"Invalid {name}.")
            self.values[name] = value.strip()
        if self.values["finish"] not in {"discuss", "specified"}:
            raise ValueError("Invalid paint preference.")
        if self.values["timing"] not in {"flexible", "soon", "1-3-months", "later"}:
            raise ValueError("Invalid timing preference.")
