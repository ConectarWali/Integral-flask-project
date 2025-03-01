# Integral Flask Project

A powerful Flask extension that provides an integrated solution for building robust web applications with WebSocket support, JWT authentication, database management, email handling, and CORS configuration.

## Features

- 🔒 Built-in JWT Authentication
- 🔌 WebSocket Support
- 📦 Database Integration with SQLAlchemy
- 📧 Email Support
- 🌐 CORS Management
- 📘 Blueprint Support
- 🔄 Environment Management
- ⚡ Singleton Pattern Implementation

## Installation

```bash
pip install integral_flask_project
```

## Quick Start

```python
from integral_flask_project import Integral_flask_project

# Create application instance
app = Integral_flask_project(__name__)

# Create an API blueprint
api = app.create_blueprint('api', url_prefix='/api')

@api.route('/hello')
def hello():
    return {'message': 'Hello World!'}

# Run the application
app.run_app(host='0.0.0.0', port=5000)
```

## Usage Examples

### WebSocket Setup

```python
from integral_flask_project import Integral_flask_project

# Create application with WebSocket support
app = Integral_flask_project(
    __name__, 
    run_type=Integral_flask_project.RUN_TYPE.SOKET_IO
)

socket = app.socket

@socket.on('connect')
def handle_connect():
    print('Client connected')

@socket.on('message')
def handle_message(data):
    socket.emit('response', {'status': 'received'})

app.run_app(host='0.0.0.0', port=5000)
```

### Database Models

```python
from integral_flask_project import Integral_flask_project

app = Integral_flask_project(__name__)
db = app.db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

# Create tables
with app.app_context():
    db.create_all()
```

you can use the command line options as:

```bash
flask db init
flask db migrate
flask db upgrade
```

### JWT Authentication

```python
from integral_flask_project import Integral_flask_project
from flask_jwt_extended import jwt_required, create_access_token

app = Integral_flask_project(__name__)
jwt = app.jwt

@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='user123')
    return {'token': access_token}

@app.route('/protected')
@jwt_required()
def protected():
    return {'message': 'Access granted'}
```

### Email Sending

```python
from integral_flask_project import Integral_flask_project
from flask_mail import Message

app = Integral_flask_project(__name__)
mail = app.mail

def send_welcome_email(to_email):
    msg = Message(
        'Welcome!',
        sender='noreply@example.com',
        recipients=[to_email]
    )
    msg.body = 'Welcome to our application!'
    mail.send(msg)
```

## Configuration

### Environment Variables

The application can be configured using environment variables or a `.env` file. Here are the available configuration options:

```env
# General Flask Config
FLASK_APP=app.py
FLASK_NAME="My Flask App"
SECRET_KEY=your-secret-key
DEBUG=True
FLASK_ENV=development

# Database Config
SQLALCHEMY_DATABASE_URI=sqlite:///development_database.sql
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Mail Config
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_password

# JWT Config
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# SocketIO Config
SOCKETIO_MESSAGE_QUEUE=redis://localhost:6379/0
SOCKETIO_CHANNEL=flask-socketio
SOCKETIO_PING_TIMEOUT=5
SOCKETIO_PING_INTERVAL=25
```

### CORS Configuration

CORS are already configured by default as: CORS(app)

### Module Auto-Loading

The library automatically loads modules from your routes and sockets directories:

```python
your_app/
├── app/
│   ├── __init__.py
│   ├── controller/
│   │   ├── __init__.py
│   ├── middleware/
│   │   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   ├── models/
│       ├── __init__.py
├── routes/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── login.py
│   │   └── register.py
│   └── api/
│       ├── __init__.py
│       └── users.py
├── sockets/
│   ├── __init__.py
│   └── chat.py
├── app.py
```

Modules are loaded recursively, so you can organize your routes and sockets in subdirectories.

## Advanced Usage

### Custom CORS Configuration

The library provides a flexible CORS manager for handling Cross-Origin Resource Sharing:

```python
from datetime import timedelta
from integral_flask_project import Integral_flask_project

app = Integral_flask_project(__name__)
cors = app.cors

#Create a custom CORS configuration for an API model
cors.create_config(
            name="api",
            origins=["*"],
            methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=[
                "Content-Type",
                "Authorization",
                "X-API-Key",
                "X-Request-ID",
                "X-Rate-Limit-Limit",
                "X-Rate-Limit-Remaining",
                "X-Rate-Limit-Reset"
            ],
            expose_headers=[
                "X-Request-ID",
                "X-Rate-Limit-Limit",
                "X-Rate-Limit-Remaining",
                "X-Rate-Limit-Reset"
            ],
            supports_credentials=True,
            max_age=timedelta(hours=1),
            header_values={
                "X-Content-Type-Options": "nosniff",
                "X-Rate-Limit-Limit": "10"
            }
        )

print(cors.configs)
# Configuration is automatically applied to all blueprint routes
```

### Environment-Specific Configuration

```python
from integral_flask_project import Integral_flask_project, Development_config, Production_config

# Development environment
app = Integral_flask_project(__name__, env=Development_config)

# Production environment
app = Integral_flask_project(__name__, env=Production_config)
```

## API Reference

### Class: Integral_flask_project

#### Constructor Parameters

- `import_name` (str): The name of the application package
- `run_type` (RUN_TYPE): Application run type (FLASK or SOCKET_IO)
- `env` (object|str|None): Environment configuration
- `path_routes` (str): Directory path for route modules
- `path_sockets` (str): Directory path for socket modules
- `static_url_path` (str|None): URL path for static files
- `static_folder` (str|PathLike[str]|None): Static files directory
- `static_host` (str|None): Host for static files
- `host_matching` (bool): Enable host matching for routes
- `subdomain_matching` (bool): Enable subdomain matching
- `template_folder` (str|PathLike[str]|None): Templates directory
- `instance_path` (str|None): Instance path
- `instance_relative_config` (bool): Use relative instance config
- `root_path` (str|None): Application root path

#### Properties

- `cors`: CORS configuration manager
- `jwt`: JWT manager
- `db`: SQLAlchemy database instance
- `migration`: Database migration manager
- `socket`: SocketIO instance
- `mail`: Flask-Mail instance

#### Methods

- `create_blueprint(name: str, **kwargs)`: Create a Flask Blueprint
- `run_app(**kwargs)`: Initialize and run the application

## Best Practices

1. **Route Organization**
   - Group related routes in blueprints
   - Use meaningful URL prefixes
   - Keep route handlers focused

2. **WebSocket Events**
   - Use namespaces for feature separation
   - Handle connection/disconnection events
   - Implement error handling

3. **Database Usage**
   - Use migrations for schema changes (you can use the command line options from Migrate)
   - Implement proper session management
   - Define clear model relationships

4. **Security**
   - Set proper JWT expiration times
   - Configure CORS appropriately
   - Use environment variables for secrets

## Error Handling

```python
from integral_flask_project import Integral_flask_project

app = Integral_flask_project(__name__)

@app.errorhandler(404)
def not_found_error(error):
    return {'error': 'Resource not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    app.db.session.rollback()
    return {'error': 'Internal server error'}, 500
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
