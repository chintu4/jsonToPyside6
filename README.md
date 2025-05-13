# Json to pyside6 convert

## Features
1. can be to load only a form in your ui
2. can be used to load only a layout from json
3. 

**I assume i could convert to**

iam putting proper json-schema 
```
{
    "QVLayout":[
        {
            "widget":"QLabel",
            "text":"ok"  
        }
    ]
}
```

the json to pyside6 build can return a to dom to build ui upon it 
the builder could be used to build just a form or just and return using build

> This can even used to build complex ui with proper ui that look first -like designed by professional
This could be used from simple ui use cases to very large use cases 
```
{
    "singleCenterwidget":[{
        "widget":"QPushButton",
        "text":"hello",
        "icon":"path/to/icon.svg"
    }
    ]
}
```
> Layout Always contains array even single center widget

```
{
   "ui":{ 
        "singleCenterwidget":
        [
            {
            "widget":"QPushButton",
            "text":"hello",
            "icon":"path/to/icon.svg"
            }
        ],
    },
    "stylesheet":"path/to/style.qss",
    "mainWindow":{
        "title":"hello"
    }
}
```
## This appoach ensure ui is built ui formly and expected manner
```
{
   "ui":{ 
        "QFrame":
        [
            {
            "widget":"QPushButton",
            "text":"hello",
            "icon":"path/to/icon.svg"
            "stylesheet":"background-color:red;color:white;"
            }
        ],
    },
    
}
```
## Extended Schema 
```
{
  "ui": {
    "singleCenterwidget": [
      {
        "widget": "QPushButton",
        "name": "my_button",
        "text": "hello",
        "icon": "path/to/icon.svg",
        "properties": {
          "toolTip": "Click me",
          "enabled": true,
          "minimumSize": [100, 30]
        },
        "events": {
          "clicked": "on_button_click"
        },
        "animations": {
          "hover": {
            "property": "geometry",
            "startValue": [10, 10, 100, 30],
            "endValue": [10, 10, 120, 30],
            "duration": 300
          }
        }
      }
    ]
  },
  "layout": {
    "type": "QVBoxLayout",
    "spacing": 10,
    "margin": 10
  },
  "stylesheet": "path/to/style.qss",
  "mainWindow": {
    "title": "hello",
    "geometry": [100, 100, 800, 600],
    "icon": "path/to/window_icon.svg"
  }
}
```


## Even Animation
Ease
animation


## To make Full Flejed Pyside6 app using json

The current schema covers basic widgets, layout, styling, and simple animations. It is not yet sufficient for a full-fledged PySide6 app with:

Nested layouts

Menus, toolbars, dock widgets

Stacked views or routing

Dialogs (modal, file, color, etc.)

Threading (QThread, QRunnable)

Models and views (QTableView, QListView, QTreeView)

MVC/MVVM patterns

Signals/slots across modules

State management

Timers and events

OpenGL/Graphics views

Complex drag/drop

Localization (via .ts files)

Multimedia (audio/video)

System tray

Clipboard, printing, networking

WebEngine support

Settings and persistence

Input validation and forms

Accessibility

## UseCase 
Build size could significatly reduced due to use of json files to load the ui

## Assumptions 
This could be used to build only ui only

```
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
## Checkbox Examples
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
