from Core.ui import StyleSheet

styles = StyleSheet({
    "container": {
        "name": "QWidget#valve_control_widget",
        "max-height": "120px",
        # "max-width": "5000px",
        # "width": "100%",
        # "height": '100%',
        # "background-color": "rgb(190, 190, 190)",
    },
    "line": {
        "height": "2px",
        "max-height": "2px",
        "width": "100%",
        "background-color": "rgb(0, 0, 0)",
    },
    "button_container": {
        "height": "100px",
        "width": "100px",
    },

})

button_style = """
QPushButton#button_valve_control {
    height: 90px;
    width: 90px;
    border-radius: 45px;
    background-color: rgb(254, 100, 100);
    border-style: solid;
    border-width: 1px;
    border-color: rgba(0,0,100,255);
}
QPushButton#button_valve_control:pressed {
    background-color: rgb(155, 100, 100);
}
"""

button_style1 = """
QWidget#button_valve_control {
    height: 90px;
    width: 90px;
    border-radius: 45px;
    background-color: rgb(254, 100, 100);
    border-style: solid;
    border-width: 1px;
    border-color: rgba(0,0,100,255);
}
QWidget#button_valve_control:pressed {
    background-color: rgb(155, 100, 100);
}
"""
