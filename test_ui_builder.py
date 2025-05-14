import unittest
from unittest.mock import MagicMock, patch
import sys
from PySide6.QtWidgets import QTableView, QApplication
from PySide6.QtGui import QStandardItemModel
from ui_builder import AppBuilder

class TestSetupViews(unittest.TestCase):
    
    @patch('ui_builder.QApplication')
    def setUp(self, mock_app):
        # Create mock QApplication instance
        self.app_instance = MagicMock()
        mock_app.instance.return_value = self.app_instance
        
        # Test config with a view
        self.config = {
            "views": [
                {
                    "type": "QTableView",
                    "model": "test_model",
                    "properties": {
                        "alternatingRowColors": True
                    }
                }
            ]
        }
        
        self.builder = AppBuilder(self.config)
        self.builder.models = {"test_model": MagicMock(spec=QStandardItemModel)}
          @patch('ui_builder.QTableView')
    def test_setup_views(self, mock_table_view):
        # Create a mock view that will be returned when QTableView is instantiated
        mock_view = MagicMock()
        mock_table_view.return_value = mock_view
        
        # Set up views - this should return the view 
        view = self.builder.setup_views()
        
        # Verify QTableView was created
        mock_table_view.assert_called_once()
        
        # Verify model was set
        mock_view.setModel.assert_called_once_with(self.builder.models["test_model"])
        
        # Verify property was set
        self.assertEqual(mock_view.alternatingRowColors, True)
        
        # Assert the returned view is our mock
        self.assertEqual(view, mock_view)
      @patch('ui_builder.QListView')
    def test_setup_views_no_model(self, mock_list_view):
        # Config with a view but no model specified
        self.builder.config = {
            "views": [
                {
                    "type": "QListView",
                    "properties": {
                        "showDropIndicator": False
                    }
                }
            ]
        }
        
        # Create a mock view
        mock_view = MagicMock()
        mock_list_view.return_value = mock_view
        
        # Set up views
        view = self.builder.setup_views()
        
        # Verify QListView was created
        mock_list_view.assert_called_once()
        
        # Verify model was NOT set (no setModel calls)
        mock_view.setModel.assert_not_called()
        
        # Verify property was set
        self.assertEqual(mock_view.showDropIndicator, False)
        
        # Assert the returned view is our mock
        self.assertEqual(view, mock_view)

if __name__ == '__main__':
    unittest.main()