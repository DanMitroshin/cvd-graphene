class StyleSheet(object):
    def __init__(self, styles: dict = None):
        self.styles = styles

    def reformat_style(self, style: dict):
        answer = ""
        name = None
        for key, value in style.items():
            if key == "name":
                name = value
                continue
            answer += f"{key}: {value};\n"
        answer = answer.strip()
        if name is not None:
            answer = f"{name} {{ {answer} }}"
        return answer

    def __getattr__ (self, item):
        style = self.styles.get(item, None)
        if style is None:
            return ""
        return self.reformat_style(style)
