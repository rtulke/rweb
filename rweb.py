#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import yaml
import sys
from flask import Flask, render_template_string, send_from_directory, abort, request

# Fallback-Values for the Flask App
FALLBACK_ALLOWED_IPS = ['127.0.0.1']                            # Default: Only allow localhost
FALLBACK_HTML_PATH = 'index.html'                               # Default: Display index.html
FALLBACK_PORT = 5000                                            # Default: Run on port 5000 (HTTP)
FALLBACK_LISTEN = '0.0.0.0'                                     # Default: Listen on all interfaces
FALLBACK_DIRECTORY = '/'                                        # Default: Serve files from root directory
FALLBACK_STATIC_DIR = 'static'                                  # Default: Serve static files from 'static' directory
FALLBACK_MESSAGE = 'Hello World!'                               # Default message to display if no HTML file is provided
USER_CONFIG_PATH = os.path.expanduser('~/.rweb/config.yaml')    # Default path in user's home directory

# Function to parse command line arguments
def parse_args():
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=60)
    parser = argparse.ArgumentParser(formatter_class=formatter, description='Flask App to display an HTML file')
    parser.add_argument('-p', '--path', type=str, help='Path to the HTML file to display')
    parser.add_argument('-P', '--port', type=int, help='Port to run the Flask server on')
    parser.add_argument('-i', '--ips', nargs='+', help='List of allowed IP addresses')
    parser.add_argument('-L', '--listen', type=str, help='IP address to listen on (default: 0.0.0.0)')
    parser.add_argument('-c', '--config', type=str, default=None, help='Path to the config file')
    parser.add_argument('-G', '--generate-config', action='store_true', help='Generate a config.yaml file with the current settings')
    parser.add_argument('-D', '--directory', type=str, help='Default directory to serve files from')
    parser.add_argument('-S', '--static-dir', type=str, help='Directory to serve static files from (e.g., images)')
    parser.add_argument('-l', '--list-config', action='store_true', help='List the current config.yaml file content and exit')
    
    return parser.parse_args()

# Function to load the config.yaml file
def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    return {}

# Function to check if the config file exists in user directory or current working directory
def get_config_path():
    # Check user directory first
    if os.path.exists(USER_CONFIG_PATH):
        return USER_CONFIG_PATH
    # Check current working directory for .rweb/config.yaml
    current_dir_config_path = os.path.join(os.getcwd(), '.rweb/config.yaml')
    if os.path.exists(current_dir_config_path):
        return current_dir_config_path
    return USER_CONFIG_PATH  # Fallback to user directory if none found

# Function to generate the config.yaml file in the current working directory
def generate_config_file(ips, path, port, listen, directory, static_dir):
    current_dir_config_dir = os.path.join(os.getcwd(), '.rweb')

    # Create the .rweb directory if it doesn't exist
    if not os.path.exists(current_dir_config_dir):
        os.makedirs(current_dir_config_dir)

    config_file = os.path.join(current_dir_config_dir, 'config.yaml')

    # Check if the config file already exists and ask the user if they want to overwrite it  
    if os.path.exists(config_file):
        overwrite = input(f"The file '{config_file}' already exists. Do you want to overwrite it? (Y/n): ")
        if overwrite.lower() not in ['y', 'yes', '']:
            print("Operation cancelled. The config file was not overwritten.")
            return

    config_data = {
        'allowed_ips': ips,
        'html_path': path,
        'port': port,
        'listen': listen,
        'default_message': 'Hello World!',
        'default_directory': directory,
        'static_directory': static_dir
    }
    with open(config_file, 'w') as file:
        yaml.dump(config_data, file)
    print(f"Config file '{config_file}' generated successfully.")

# Function to list the current config.yaml file content
def list_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            print("Current configuration:")
            print(yaml.dump(config_data, default_flow_style=False))
    else:
        print(f"No config file found at {config_file}")

# Limit the remote address to the allowed IPs from the config file or command line
def limit_remote_addr():
    if allowed_ips:
        client_ip = request.remote_addr
        if client_ip not in allowed_ips:
            abort(403)  # Verboten

# User-defined error page for 403 Forbidden
def forbidden(e):
    client_ip = request.remote_addr
    return render_template_string(f'''
        <h1>Forbidden</h1>
        <p>Your IP address {client_ip} is not allowed to access this resource.</p>
        <p>Please contact the server administrator to add your IP address to the allowed list in the config.yaml file.</p>
    '''), 403

# User-defined error page for 404 Not Found
def not_found(e):
    return render_template_string(f'''
        <h1>File Not Found</h1>
        <p>The file you requested could not be found on the server.</p>
        <p>Requested file: {html_path}</p>
        <p>Please check the path and try again.</p>
    '''), 404

# Main function to run the Flask app
if __name__ == '__main__':
    args = parse_args()

    # Determine the correct config file path
    config_file = args.config if args.config else get_config_path()

    # Load the configuration from the config file
    config = load_config(config_file)

    # Show the current config file content and exit
    if args.list_config:
        list_config(config_file)
        sys.exit(0)

    # Set the configuration values from the command line arguments or the config file
    allowed_ips = args.ips if args.ips else config.get('allowed_ips', FALLBACK_ALLOWED_IPS)
    html_path = args.path if args.path else config.get('html_path', FALLBACK_HTML_PATH)
    port = args.port if args.port else config.get('port', FALLBACK_PORT)
    listen = args.listen if args.listen else config.get('listen', FALLBACK_LISTEN)
    default_directory = args.directory if args.directory else config.get('default_directory', FALLBACK_DIRECTORY)
    static_dir = args.static_dir if args.static_dir else config.get('static_directory', FALLBACK_STATIC_DIR)
    default_message = config.get('default_message', FALLBACK_MESSAGE)

    # If the user wants to generate a config file, do it and exit
    if not args.generate_config:
        if os.path.exists(config_file):
            print(f"Loaded configuration from: {config_file}")
        else:
            print("No configuration file loaded. Using fallback values:")
            print(f"Allowed IPs: {allowed_ips}")
            print(f"HTML Path: {html_path}")
            print(f"Port: {port}")
            print(f"Listen: {listen}")
            print(f"Default Directory: {default_directory}")
            print(f"Static Directory: {static_dir}")
            print(f"Default Message: {default_message}")

        # Check if the user is trying to bind to a port below 1024 without root privileges
        if port < 1024 and os.geteuid() != 0:
            print("Error: You must run this script as root to bind to ports below 1024.")
            sys.exit(1)  # Beenden des Skripts

    # Start the Flask app
    if args.generate_config:
        generate_config_file(allowed_ips, html_path, port, listen, default_directory, static_dir)
    else:
        app = Flask(__name__, static_folder=static_dir)
        app.before_request(limit_remote_addr)
        app.errorhandler(403)(forbidden)
        app.errorhandler(404)(not_found)

        # Serve static files from the 'static' directory
        @app.route('/')
        def show_page():
            if html_path:
                directory, filename = os.path.split(html_path)
                if os.path.exists(html_path):
                    return send_from_directory(directory, filename)
                else:
                    abort(404)
            else:
                return render_template_string(default_message)

        app.run(debug=True, port=port, host=listen)
