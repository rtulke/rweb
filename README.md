# rweb
Just a very simple Webserver for single HTML Sites

This rweb (Roberts WebServer) is a simple Flask application that allows you to display an single HTML file configured via a YAML configuration file or command-line arguments. When developing some of my smaller projects I needed a quick way to configure a simple web server that can do nothing more than display a simple html file.
The server port, allowed IP addresses, HTML file path, listening IP, and default HTML content can be configured through `config.yaml`. If a command-line argument is provided, it overrides the respective setting in the `config.yaml`. If neither a config file nor arguments are provided, the script falls back to default variables. A config file can be generated with the `--generate-config` (`-G`) option.

## Setup

```bash
sudo apt update && apt upgrade
sudo apt install -y  git
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/rtulke/rweb.git
cd rweb
cp rweb.py rweb
chmod +x rweb
sudo cp rweb /usr/local/bin
```

## Configure rweb

To create a simple webserver configuration in YAML format you only need the option -G

```bash
rweb -G
```

```
Config file 'config.yaml' generated successfully.
```

Default values are now entered here.

```bash
cat config.yaml
```

```
allowed_ips:
- 127.0.0.1
listen: 0.0.0.0
port: 5000
default_message: Hello World!
default_directory: /
html_path: index.html
static_directory: static
```

You can now edit the config.yaml yourself and make further adjustments. An example.

```bash
vim config.yaml
```

```
allowed_ips:
- 127.0.0.1
- 10.0.0.2
- 192.168.1.10
listen: 0.0.0.0
port: 8080
default_message: Hello World!
default_directory: /
html_path: /home/myuser/pdiff/index.html
static_directory: /home/myuser/pdiff/static
```

For example, you can determine which IP addresses you want to allow access to the web server.

Alternatively, you can also specify the config.yaml configuration as a parameter.

```bash
rweb -G -i 10.10.10.2 127.0.0.1 192.168.10.10 -L 10.0.0.1 -P 8080
```

rweb will now read your parameters and write them directly to the config.yaml file.

```
The file 'config.yaml' already exists. Do you want to overwrite it? (Y/n): Y
Config file 'config.yaml' generated successfully.
```

```bash
cat config.yaml

```

As you can see, only the things that were handed over as parameters were adapted. The previously created configurations are not touched.

```
allowed_ips:
- 10.10.10.2
- 127.0.0.1
- 192.168.10.10
default_message: Hello World!
html_path: /home/robert/test.html
listen: 10.0.0.1
port: 8080
```

If the -G parameter is omitted, the parameters are interpreted as start input and the web server starts with these parameters.

```bash
./rweb -i 10.10.10.2 127.0.0.1 192.168.10.10 -L 10.10.10.4 -P 8080
```

```
 * Serving Flask app 'rweb'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://10.10.10.4:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 645-305-611
```



## Command-Line Arguments

~~~
usage: rweb2.py [-h] [-p PATH] [-P PORT] [-i IPS [IPS ...]] [-L LISTEN] [-c CONFIG] [-G] [-D DIRECTORY] [-S STATIC_DIR] [-l]

Flask App to display an HTML file

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to the HTML file to display
  -P PORT, --port PORT  Port to run the Flask server on
  -i IPS [IPS ...], --ips IPS [IPS ...]
                        List of allowed IP addresses
  -L LISTEN, --listen LISTEN
                        IP address to listen on (default: 0.0.0.0)
  -c CONFIG, --config CONFIG
                        Path to the config file
  -G, --generate-config
                        Generate a config.yaml file with the current settings
  -D DIRECTORY, --directory DIRECTORY
                        Default directory to serve files from
  -S STATIC_DIR, --static-dir STATIC_DIR
                        Directory to serve static files from (e.g., images)
  -l, --list-config     List the current config.yaml file content and exit
~~~
