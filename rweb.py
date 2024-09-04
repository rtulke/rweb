#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import yaml
import sys
import socket
from flask import Flask, render_template_string, send_from_directory, abort, request

# Function for generating the help message for fallback
def parse_args():
    parser = argparse.ArgumentParser(description='Flask App to display an HTML file')
    parser.add_argument('-p', '--path', type=str, help='Path to the HTML file to display')
    parser.add_argument('-P', '--port', type=int, help='Port to run the Flask server on')
    parser.add_argument('-i', '--ips', nargs='+', help='List of allowed IP addresses')
    parser.add_argument('-L', '--listen', type=str, help='IP address to listen on (default: 0.0.0.0)')
    parser.add_argument('-c', '--config', type=str, default=None, help='Path to the config file')
    parser.add_argument('-G', '--generate-config', action='store_true', help='Generate a config.yaml file with the current settings')
    parser.add_argument('-D', '--directory', type=str, help='Default directory to serve files from')
    parser.add_argument('-S', '--static-dir', type=str, help='Directory to serve static files from (e.g., images)')
    
    return parser.parse_args()

# Function for loading the configuration from the YAML file
def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    return {}

# Function for generating the config.yaml file
def generate_config_file(config_file, ips, path, port, listen, directory, static_dir):
    config_dir = os.path.dirname(config_file)

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
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

# Check whether the port is already in use
def check_port_in_use(port, host="0.0.0.0"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
        except OSError:
            return True
    return False

# Function for restricting access on an IP basis
def limit_remote_addr():
    if allowed_ips:
        client_ip = request.remote_addr
        if client_ip not in allowed_ips:
            abort(403)  # Not allowdd

# Custom error page for 403 Forbidden
def forbidden(e):
    client_ip = request.remote_addr
    return render_template_string(f'''
        <h1>Forbidden</h1>
        <p>Your IP address {client_ip} is not allowed to access this resource.</p>
        <p>Please contact the server administrator to add your IP address to the allowed list in the config.yaml file.</p>
    '''), 403

# Custom error page for 404 Not Found
def not_found(e):
    return render_template_string(f'''
        <h1>File Not Found</h1>
        <p>The file you requested could not be found on the server.</p>
        <p>Requested file: {html_path}</p>
        <p>Please check the path and try again.</p>
    '''), 404

if __name__ == '__main__':
    args = parse_args()

    config_file = None

    if os.geteuid() == 0:  # Checks whether the user is root
        if args.config:
            config_file = args.config
        else:
            config_file = '/etc/rweb/config.yaml'
            if not os.path.exists(config_file):
                config_file = os.path.expanduser('~/.rweb/config.yaml')
    else:
        config_file = args.config if args.config else 'config.yaml'

    config = load_config(config_file)

    allowed_ips = args.ips if args.ips else config.get('allowed_ips', ['127.0.0.1'])
    html_path = args.path if args.path else config.get('html_path', '')
    port = args.port if args.port else config.get('port', 5000)
    listen = args.listen if args.listen else config.get('listen', '0.0.0.0')
    default_directory = args.directory if args.directory else config.get('default_directory', '/')
    static_dir = args.static_dir if args.static_dir else config.get('static_directory', 'static')
    default_message = config.get('default_message', 'Hello World!')

    # Check whether the user is trying to use a port below 1024 without root rights
    if port < 1024 and os.geteuid() != 0:
        print("Error: You must run this script as root to bind to ports below 1024. To run the script as a user you must select a port higher than 1024.")
        sys.exit(1)  # Beenden des Skripts

    # Check whether the port is already in use
    if check_port_in_use(port, listen):
        print(f"Error: The port {port} is already in use by another application.")
        sys.exit(1) 

    app = Flask(__name__, static_folder=static_dir)

    app.before_request(limit_remote_addr)
    app.errorhandler(403)(forbidden)
    app.errorhandler(404)(not_found)  # Custom 404 handler

    # Route for the standard page
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

    if args.generate_config:
        generate_config_file(config_file, allowed_ips, html_path, port, listen, default_directory, static_dir)
    else:
        app.run(debug=True, port=port, host=listen)
