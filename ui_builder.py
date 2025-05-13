import sys
import json
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class AppBuilder:    
    def __init__(self, json_config):
        self.config = json_config
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.widgets = {}
        self.models = {}
        self.functions = self.config.get("functions", {})
        
    def build(self):
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("JSON UI Application")
        self.main_window.setGeometry(100, 100, 800, 600)
        self.setup_central_ui()
        if "stylesheet" in self.config:
            self.app.setStyleSheet(open(self.config["stylesheet"]).read())
        self.main_window.show()
        sys.exit(self.app.exec())

    def setup_main_window(self):
        conf = self.config["mainWindow"]
        self.main_window.setWindowTitle(conf.get("title", "App"))
        self.main_window.setGeometry(*conf.get("geometry", [100, 100, 800, 600]))
        if "icon" in conf:
            self.main_window.setWindowIcon(QIcon(conf["icon"]))

    def setup_menus(self):
        for menu_conf in self.config.get("menus", []):
            menu = self.main_window.menuBar().addMenu(menu_conf["title"])
            for action_conf in menu_conf.get("actions", []):
                action = QAction(action_conf["text"], self.main_window)
                if "shortcut" in action_conf:
                    action.setShortcut(action_conf["shortcut"])
                if "event" in action_conf:
                    action.triggered.connect(lambda checked=False, e=action_conf["event"]: self.run_script(e))
                menu.addAction(action)

    def setup_toolbars(self):
        for tb_conf in self.config.get("toolbars", []):
            toolbar = QToolBar(tb_conf.get("title", ""))
            for act in tb_conf.get("actions", []):
                btn = QAction(QIcon(act.get("icon", "")), "", self.main_window)
                btn.setToolTip(act.get("tooltip", ""))
                btn.triggered.connect(lambda checked=False, e=act["event"]: self.run_script(e))
                toolbar.addAction(btn)
            self.main_window.addToolBar(toolbar)

    def setup_models(self):
        for model_conf in self.config.get("models", []):
            if model_conf["type"] == "QStandardItemModel":
                model = QStandardItemModel()
                model.setHorizontalHeaderLabels(model_conf.get("headers", []))
                for row in model_conf.get("data", []):
                    items = [QStandardItem(str(cell)) for cell in row]
                    model.appendRow(items)
                self.models[model_conf["name"]] = model

    def setup_central_ui(self):
        widget = self.build_layout(self.config["layout"])
        if "name" in self.config:
            self.widgets[self.config["name"]] = widget
        self.main_window.setCentralWidget(widget)

    def build_layout(self, layout_conf):
        layout_type = layout_conf["type"]
        layout_cls = globals()[layout_type]
        layout = layout_cls()
        
        # Apply layout properties
        if "properties" in layout_conf:
            for prop, val in layout_conf["properties"].items():
                if prop == "alignment":
                    layout.setAlignment(getattr(Qt, val))
                elif prop == "spacing":
                    layout.setSpacing(val)
                elif prop == "margin":
                    layout.setContentsMargins(val, val, val, val)
                else:
                    try:
                        setter = getattr(layout, f"set{prop[0].upper()}{prop[1:]}")
                        setter(val)
                    except AttributeError:
                        print(f"Warning: Property {prop} not applied to layout")
        
        container = QWidget()
        container.setLayout(layout)
        
        for child in layout_conf.get("children", []):
            widget_cls = globals().get(child["widget"], QLabel)
            widget = widget_cls()
            
            if "text" in child:
                widget.setText(child.get("text", ""))
            
            if "name" in child:
                self.widgets[child["name"]] = widget
            
            if "properties" in child:
                for prop, val in child["properties"].items():
                    if prop == "styleSheet":
                        widget.setStyleSheet(val)
                    elif prop == "placeholderText":
                        if hasattr(widget, "setPlaceholderText"):
                            widget.setPlaceholderText(val)
                    elif prop == "echoMode" and hasattr(widget, "setEchoMode"):
                        widget.setEchoMode(getattr(QLineEdit, val))
                    elif prop == "alignment":
                        widget.setAlignment(getattr(Qt, val))
                    else:
                        try:
                            if hasattr(Qt, val) and isinstance(val, str):
                                setattr(widget, prop, getattr(Qt, val))
                            else:
                                setter = getattr(widget, f"set{prop[0].upper()}{prop[1:]}")
                                setter(val)
                        except (AttributeError, TypeError):
                            print(f"Warning: Property {prop} not applied to {child['widget']}")
            
            if "events" in child:
                for signal, script in child["events"].items():
                    getattr(widget, signal).connect(lambda checked=False, s=script: self.run_script(s))
            
            layout.addWidget(widget)
        
        return container

    def setup_dialogs(self):
        for dlg_conf in self.config.get("dialogs", []):
            if dlg_conf["type"] == "QMessageBox":
                box = QMessageBox()
                box.setWindowTitle(dlg_conf["title"])
                box.setText(dlg_conf["text"])
                box.setIcon(getattr(QMessageBox, dlg_conf["icon"]))
                for btn in dlg_conf["buttons"]:
                    box.addButton(btn, QMessageBox.AcceptRole)
                self.widgets[dlg_conf["name"]] = box
            elif dlg_conf["type"] == "QDialog":
                dialog = QDialog()
                dialog.setWindowTitle(dlg_conf["title"])
                layout = self.build_layout(dlg_conf["layout"])
                dialog.setLayout(layout.layout())
                self.widgets[dlg_conf["name"]] = dialog

    def setup_views(self):
        for view_conf in self.config.get("views", []):
            view_cls = globals()[view_conf["type"]]
            view = view_cls()
            model_name = view_conf.get("model")
            if model_name:
                view.setModel(self.models[model_name])
            for prop, val in view_conf.get("properties", {}).items():
                setattr(view, prop, val)
            self.main_window.setCentralWidget(view)

    def run_script(self, key):
        func_or_script = self.functions.get(key, {}).get("script")
        if func_or_script:
            try:
                if callable(func_or_script):
                    # If it's a function, call it directly
                    func_or_script()
                else:
                    # If it's a string, execute it
                    local_ctx = {"main_window": self.main_window, **self.widgets}
                    exec(func_or_script, {}, local_ctx)
            except Exception as e:
                print("Error in script:", e)

    def register_function(self, name, func):
        self.functions[name] = {"script": func}

def on_login_pressed():
    print("Login button pressed")

if __name__ == '__main__':
    
    with open("json-schema.json", encoding="utf-8") as f:
        schema = json.load(f)
    builder = AppBuilder(schema)
    builder.register_function("on_login_pressed", on_login_pressed)
    builder.build()
