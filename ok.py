import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget, QFormLayout,
    QTableView, QStandardItemModel, QStandardItem, QMessageBox
)
from PySide6.QtCore import Qt


class JSONWidgetParser:
    def __init__(self, json_data):
        self.json_data = json_data
        self.functions = {}

    def parse(self):
        main_window_data = self.json_data.get("mainWindow", {})
        self.main_window = QWidget()
        self.main_window.setWindowTitle(main_window_data.get("title", "App"))
        self.main_window.setGeometry(*main_window_data.get("geometry", [100, 100, 800, 600]))
        
        # Apply stylesheet
        if "stylesheet" in main_window_data:
            with open(main_window_data["stylesheet"], 'r') as file:
                self.main_window.setStyleSheet(file.read())

        # Parse centralWidget (main UI)
        self.parse_widget(main_window_data.get("centralWidget", {}))
        return self.main_window

    def parse_widget(self, widget_data):
        widget_type = widget_data.get("type")
        widget_class = globals().get(widget_type)
        if widget_class:
            widget = widget_class()
            self.setup_widget_properties(widget, widget_data)
            self.setup_widget_layout(widget, widget_data)

            # Add widget to layout or parent container
            if isinstance(widget, QWidget):
                layout = QVBoxLayout()  # Default layout
                layout.addWidget(widget)
                self.main_window.setLayout(layout)
            return widget
        return None

    def setup_widget_properties(self, widget, widget_data):
        for prop, value in widget_data.get("properties", {}).items():
            if prop == "styleSheet":
                widget.setStyleSheet(value)
            else:
                widget.setProperty(prop, value)

    def setup_widget_layout(self, widget, widget_data):
        layout_data = widget_data.get("layout")
        if layout_data:
            layout_type = layout_data.get("type")
            layout_class = globals().get(layout_type)
            if layout_class:
                layout = layout_class()
                self.setup_layout_properties(layout, layout_data)

                for child_data in layout_data.get("children", []):
                    child_widget = self.parse_widget(child_data)
                    if child_widget:
                        layout.addWidget(child_widget)

                if isinstance(widget, QWidget):
                    widget.setLayout(layout)

    def setup_layout_properties(self, layout, layout_data):
        for prop, value in layout_data.get("properties", {}).items():
            layout.setProperty(prop, value)

    def setup_widget_events(self, widget, widget_data):
        events = widget_data.get("events", {})
        for event, handler in events.items():
            if event == "clicked":
                self.setup_event_handler(widget, event, handler)

    def setup_event_handler(self, widget, event, handler):
        if hasattr(widget, event):
            method = getattr(self, handler, None)
            if method:
                widget.clicked.connect(method)

    def on_button_click(self):
        print("Button clicked")


# Example Usage:
if __name__ == "__main__":
    app = QApplication([])

    # Example JSON schema
    json_schema = '''
    {
      "mainWindow": {
        "title": "Button Example",
        "geometry": [100, 100, 400, 300],
        "icon": "assets/app_icon.svg",
        "stylesheet": "styles/app.qss",
        "centralWidget": {
          "type": "QWidget",
          "layout": {
            "type": "QVBoxLayout",
            "children": [
              {
                "widget": "QPushButton",
                "name": "actionButton",
                "text": "Click Me",
                "properties": {
                  "styleSheet": "background-color: #3498db; color: white; padding: 10px;"
                },
                "events": {
                  "clicked": "on_button_click"
                }
              }
            ]
          }
        }
      }
    }
    '''

    json_data = json.loads(json_schema)
    parser = JSONWidgetParser(json_data)
    window = parser.parse()
    window.show()

    app.exec()
