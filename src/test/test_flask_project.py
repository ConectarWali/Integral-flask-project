import unittest
from unittest.mock import Mock, patch
from integral_flask_project import Integral_flask_project

class TestIntegralFlaskProject(unittest.TestCase):
    @patch('src.App_config')
    def setUp(self, mock_app_config):
        """Set up test cases"""
        # Mock the necessary components
        self.mock_jwt = Mock()
        self.mock_db = Mock()
        self.mock_socket = Mock()
        self.mock_mail = Mock()
        self.mock_migration = Mock()
        
        # Configure app_config mock
        mock_app_config.return_value.create_app.return_value = (
            self.mock_jwt,
            (self.mock_db, self.mock_migration),
            self.mock_socket,
            self.mock_mail
        )
        
        # Create app instance
        self.app = Integral_flask_project(__name__)

    def test_singleton_pattern(self):
        """Test that the class follows singleton pattern"""
        app2 = Integral_flask_project(__name__)
        self.assertIs(self.app, app2)

    def test_property_access(self):
        """Test accessing various properties"""
        self.assertEqual(self.app.jwt, self.mock_jwt)
        self.assertEqual(self.app.db, self.mock_db)
        self.assertEqual(self.app.socket, self.mock_socket)
        self.assertEqual(self.app.mail, self.mock_mail)
        self.assertEqual(self.app.migration, self.mock_migration)

    def test_create_blueprint(self):
        """Test blueprint creation"""
        blueprint = self.app.create_blueprint('test', url_prefix='/test')
        self.assertEqual(blueprint.name, 'test')
        self.assertEqual(blueprint.url_prefix, '/test')

    def test_run_app_flask_mode(self):
        """Test running app in Flask mode"""
        with patch.object(self.app, 'run') as mock_run:
            self.app.run_app(host='0.0.0.0', port=5000)
            mock_run.assert_called_once_with(host='0.0.0.0', port=5000)

    def test_run_app_socketio_mode(self):
        """Test running app in SocketIO mode"""
        app = Integral_flask_project(
            __name__, 
            run_type=Integral_flask_project.RUN_TYPE.SOKET_IO
        )
        
        with patch.object(app, 'run') as mock_run:
            with patch.object(app.socket, 'run') as mock_socket_run:
                app.run_app(host='0.0.0.0', port=5000)
                mock_run.assert_called_once_with(host='0.0.0.0', port=5000)
                mock_socket_run.assert_called_once()

    def test_run_type_enum(self):
        """Test RUN_TYPE enum values"""
        self.assertEqual(
            Integral_flask_project.RUN_TYPE.FLASK.value,
            'flask'
        )
        self.assertEqual(
            Integral_flask_project.RUN_TYPE.SOKET_IO.value,
            'socket'
        )

    @patch('os.path.exists')
    @patch('src.integral_flask_project.import_moduls')
    def test_import_modules(self, mock_import_moduls, mock_exists):
        """Test module importing"""
        mock_exists.return_value = True
        
        self.app.run_app()
        
        self.assertEqual(mock_import_moduls.call_count, 2)
        mock_import_moduls.assert_any_call('routes')
        mock_import_moduls.assert_any_call('sockets')

if __name__ == '__main__':
    unittest.main()