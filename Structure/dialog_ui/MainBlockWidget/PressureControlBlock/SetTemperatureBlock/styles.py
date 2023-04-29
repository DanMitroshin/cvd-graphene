from coregraphene.ui import StyleSheet
from Structure.dialog_ui.constants import LIGHT_GREEN

styles = StyleSheet({
    "container": {
        # "name": "QWidget",
        # "width": '300px',
        # "min-width": '300px',
        # "width": '100%',
        # "max-width": "390px",
        "background-color": "rgb(255, 255, 255)",
        # "border-radius": "14px",
        "max-height": "150px",
    },
    "title": {
        "font-size": "32px",
        "font-weight": "bold",
    },
    "label": {
        "font-size": "28px",
        # "background-color": "green",
        # "min-width": '10px',
        "max-width": '60px',
        # "width": '60px',
        # "border-radius": "0px",
    },
    "input": {
        # "border-radius": "0px",
        "font-size": "28px",
        # "background-color": "rgb(210, 210, 210)",
        "background-color": LIGHT_GREEN,
        "width": "100%",
        # "max-width": "100px",
    }
})
