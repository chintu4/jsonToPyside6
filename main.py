import json
import ui_builder

def on_login_pressed():
    print("Login button pressed")

def main():
    import sys
    from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
    from PySide6.QtCore import Qt

    app = QApplication()
    app.setStyleSheet("style.qss")
    # app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    with open("ui.json", encoding="utf-8") as f:
        schema = json.load(f)
    layout=QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.setAlignment(Qt.AlignTop)
    ok=QPushButton("ok")
    ok.setAttribute(Qt.WA_StyledBackground, True)

    layout.addWidget(ok)
    builder = ui_builder.AppBuilder(schema)
    builder.register_function("on_login_pressed", on_login_pressed)
    container = builder.build_layout(schema["layout"])
    layout.addWidget(container)
    window = QWidget()
    window.setLayout(layout)
    window.setWindowTitle("UI Builder Example")
    window.setGeometry(100, 100, 800, 600)  
    window.show()
    # window.setAttribute(Qt.WA_DeleteOnClose)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()