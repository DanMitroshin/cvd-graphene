from Core.ui import StyleSheet

styles = StyleSheet({
    "container": {
        # "name": "QWidget",
        # "max-width": "240px",
        "max-height": "170px",
        "background-color": "rgb(255, 255, 255)",
        "border-radius": "14px",
    },
    "title": {
        "font-size": "30px",
        "font-weight": "bold",
        # "text-align": "center",
    },
    "button_on": {
        "height": "70px",
        "width": "70px",
        "border-radius": "35px",
        "background-color": "rgb(0, 255, 0)",
        "border-style": "solid",
        "border-width": "1px",
        "border-color": "rgba(0,0,100,255)",
    },
    "button_off": {
        "height": "70px",
        "width": "70px",
        "border-radius": "35px",
        "background-color": "rgb(255, 0, 0)",
        "border-style": "solid",
        "border-width": "1px",
        "border-color": "rgba(0,0,100,255)",
    },
    "settings_button": {
        "height": "70px",
        "font-size": "20px",
        "background-color": "rgb(255, 255, 230)",
    },
    "run_recipe_button": {
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": "rgb(150, 255, 150)",
    },
    "edit_recipe_button": {
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": "rgb(150, 255, 150)",
    },
})

button_on_style = """
QPushButton {
    height: 70px;
    width: 70px;
    border-radius: 35px;
    background-color: rgb(0, 255, 0);
    border-style: solid;
    border-width: 1px;
    border-color: rgba(0,0,100,255);
}
QPushButton:pressed {
    background-color: rgb(0, 155, 0);
}
"""

button_off_style = """
QPushButton {
    height: 70px;
    width: 70px;
    border-radius: 35px;
    background-color: rgb(255, 0, 0);
    border-style: solid;
    border-width: 1px;
    border-color: rgba(0,0,100,255);
}
QPushButton:pressed {
    background-color: rgb(155, 0, 0);
}
"""
