from website import create_app
from website.config import DevelopmentConfig

app = create_app(DevelopmentConfig())

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='MemeBank', description='Run the MemeBank Flask web application.')
    parser.add_argument('-p', '--port', type=int, default=app.config['APP_PORT'], help=f'Port to run the server on (default: {app.config["APP_PORT"]})')
    args = parser.parse_args()
    app.run(debug=True, port=args.port)
