# JSON-PySide6 UI Builder

A dynamic UI builder for PySide6 applications that creates interfaces from JSON specifications.

## Features
1. Define entire UIs using JSON
2. Load only a form or layout component from JSON
3. Integrate JSON-defined UI components into existing applications
4. Style widgets using QSS 
5. Connect Python functions to widget events
6. Support for advanced features like models, views, dialogs, etc.

## Overview

This project allows you to define PySide6 user interfaces using JSON schemas instead of writing Qt code directly.

### Example Schema
```json
{
  "name": "loginPage",
  
  "layout": {
    "type": "QVBoxLayout",        
    "properties": {
      "alignment": "AlignCenter",
      "spacing": 20,             
      "margin": 40            
    },
    "children": [
      {
        "widget": "QLabel",      
        "name": "titleLabel",    
        "text": "🔐 Login to MyApp",
        "properties": {
          "alignment": "AlignCenter",
          "styleSheet": "font-size:24px; font-weight:bold;"
        }
      }
    ]
  }
}
```

## Example Usage

```python
import json
from ui_builder import AppBuilder

def on_login_pressed():
    print("Login button pressed")

# Load UI schema from JSON file
with open("ui.json", encoding="utf-8") as f:
    schema = json.load(f)

# Create builder and register event handlers
builder = AppBuilder(schema)
builder.register_function("on_login_pressed", on_login_pressed)

# Build and run the application
builder.build()
```

## Using with Existing Applications

You can integrate JSON-defined UI components into existing applications:

```python
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from ui_builder import AppBuilder

# Create your application and main window
app = QApplication()
window = QWidget()
layout = QVBoxLayout()

# Load UI schema
with open("ui.json", encoding="utf-8") as f:
    schema = json.load(f)

# Create builder 
builder = AppBuilder(schema)
builder.register_function("on_login_pressed", on_login_pressed)

# Get just the UI component from JSON
ui_component = builder.build_layout(schema["layout"])

# Add it to your existing layout
layout.addWidget(ui_component)
window.setLayout(layout)
window.show()

# Run the application
app.exec()
```
## QSS Styling

To apply QSS styles to your application:

1. Create a QSS file with your styles
2. In your main.py, load the file:

```python
app = QApplication()
try:
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
except FileNotFoundError:
    print("Warning: style.qss file not found")
```

## Advanced Features

The framework supports many advanced Qt features through JSON configuration:

### Layout Types
- QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout

### Widgets
- QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, etc.

### Events
Connect events to Python functions:
```json
"events": {
  "clicked": "on_login_pressed"  
}
### Models and Views

The schema supports defining data models and views:

```json
"models": [
  {
    "type": "QStandardItemModel",
    "name": "tableModel",
    "headers": ["ID", "Name", "Status"],
    "data": [
      [1, "Alice", "Active"],
      [2, "Bob", "Inactive"]
    ]
  }
],

"views": [
  {
    "type": "QTableView",
    "model": "tableModel",
    "properties": {
      "alternatingRowColors": true
    }
  }
]
```

### Dialogs

Define message boxes and custom dialogs:

```json
"dialogs": [
  {
    "type": "QMessageBox",
    "name": "infoDialog",
    "title": "Information",
    "text": "Action completed",
    "icon": "Information",
    "buttons": ["Ok"]
  }
]
```

### Menus and Toolbars

```json
"menus": [
  {
    "title": "File",
    "actions": [
      { "text": "Open", "event": "on_open_file", "shortcut": "Ctrl+O" },
      { "text": "Exit", "event": "on_exit" }
    ]
  }
],

"toolbars": [
  {
    "title": "Main",
    "actions": [
      { "icon": "icons/save.svg", "tooltip": "Save", "event": "on_save" }
    ]
  }
]
```

## Running Tests

```powershell
python test_ui_builder.py
```

### Complete Application Example

```json
{
  "mainWindow": {
    "title": "MyApp",
    "geometry": [100, 100, 800, 600],
    "icon": "assets/app_icon.svg",
    "splash-icon":"assets/app_icon.svg"
  },

  "stylesheet": "styles/app.qss",

  "menus": [
    {
      "title": "File",
      "actions": [
        { "text": "Open", "event": "on_open_file", "shortcut": "Ctrl+O" },
        { "text": "Exit", "event": "on_exit" }
      ]
    }
  ],

  "toolbars": [
    {
      "title": "Main",
      "actions": [
        { "icon": "icons/save.svg", "tooltip": "Save", "event": "on_save" }
      ]
    }
  ],

  "ui": {
    "centralWidget": {
      "type": "QStackedWidget",
      "pages": [
        {
          "name": "homePage",
          "layout": {
            "type": "QVBoxLayout",
            "children": [
              {
                "widget": "QLabel",
                "text": "Welcome",
                "properties": {
                  "alignment": "AlignCenter"
                }
              },
              {
                "widget": "QPushButton",
                "text": "Next",
                "events": {
                  "clicked": "go_to_settings"
                },
                "animations": {
                  "hover": {
                    "property": "geometry",
                    "startValue": [100, 100, 100, 40],
                    "endValue": [100, 100, 120, 40],
                    "duration": 300,
                    "easingCurve": "OutBounce"
                  }
                }
              }
            ]
          }
        },
        {
          "name": "settingsPage",
          "layout": {
            "type": "QFormLayout",
            "children": [
              {
                "widget": "QLineEdit",
                "name": "usernameField",
                "label": "Username"
              },
              {
                "widget": "QCheckBox",
                "text": "Enable notifications"
              }
            ]
          }
        }
      ]
    }
  },

  "dialogs": [
    {
      "type": "QMessageBox",
      "name": "infoDialog",
      "title": "Information",
      "text": "Action completed",
      "icon": "Information",
      "buttons": ["Ok"]
    },
    {
      "type": "QDialog",
      "name": "customDialog",
      "title": "Advanced",
      "layout": {
        "type": "QVBoxLayout",
        "children": [
          {
            "widget": "QLabel",
            "text": "Enter data"
          },
          {
            "widget": "QLineEdit",
            "name": "inputBox"
          },
          {
            "widget": "QPushButton",
            "text": "Submit",
            "events": {
              "clicked": "submit_dialog_data"
            }
          }
        ]
      }
    }
  ],

  "models": [
    {
      "type": "QStandardItemModel",
      "name": "tableModel",
      "headers": ["ID", "Name", "Status"],
      "data": [
        [1, "Alice", "Active"],
        [2, "Bob", "Inactive"]
      ]
    }
  ],

  "views": [
    {
      "type": "QTableView",
      "model": "tableModel",
      "properties": {
        "alternatingRowColors": true
      }
    }
  ],

  "functions": {
    "on_open_file": {
      "script": "print('File opened')"
    },
    "go_to_settings": {
      "script": "main_window.centralWidget().setCurrentIndex(1)"
    },
    "submit_dialog_data": {
      "script": "print('Submitted:', inputBox.text())"
    }
  }
}
```

### Checkbox Examples

```json
{
    "ui": {
        "checkboxGroup": [
            {
                "widget": "QCheckBox",
                "text": "Option 1",
                "checked": true,
                "events": {
                    "stateChanged": "on_option1_changed"
                }
            },
            {
                "widget": "QCheckBox",
                "text": "Option 2",
                "checked": false,
                "properties": {
                    "tristate": true,
                    "toolTip": "Select this option for additional features"
                }
            },
            {
                "widget": "QCheckBox",
                "text": "Disabled Option",
                "properties": {
                    "enabled": false
                }
            }
        ]
    },
    "functions": {
        "on_option1_changed": {
            "script": "print('Option 1 state changed:', sender.isChecked())"
        }
    }
}
```
