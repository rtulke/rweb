# rweb
Just a very simple Webserver for single HTML Sites

This rweb (Roberts WebServer) is a simple Flask application that allows you to display an single HTML file configured via a YAML configuration file or command-line arguments. When developing some of my smaller projects I needed a quick way to configure a simple web server that can do nothing more than display a simple html file.

The server port, allowed IP addresses, HTML file path, listening IP, and default HTML content can be configured through `config.yaml`. If a command-line argument is provided, it overrides the respective setting in the `config.yaml`. If neither a config file nor arguments are provided, the script falls back to default variables. A config file can be generated with the `--generate-config` (`-G`) option.


## Setup


### Setting up a development environment

Not absolutely necessary because you can also download the repo as tar.gz.

### Git installation

```
sudo apt update && apt upgrade
sudo apt install -y git
```

If you want to check in your changes for the rweb project via git, you should also enter your name and e-mail address for git.

```
git config --global user.name "Your Name"
git config --global user.email "your@email-address.com"
```

## Setup rweb

### Installation of the required Python3 modules

There are some modules that need to be installed additionally. The other modules used by rweb should already have been set up by the Python installation.

```
pip3 install flask yaml arparse
```

```
mkdir -p ~/dev/
cd ~/dev/
git clone https://github.com/rtulke/rweb.git
```

We have now downloaded rweb and it is located in the ~/dev directory below your user directory. If you want to execute rweb as a command, you should make the following adjustments. Otherwise you would always have to write `python3 rweb.py <param> <arg>.`


```
mkdir -p ~/bin/
cd ~/dev/rweb
cp rweb.py ~/bin/rweb
chmod +x ~/bin/rweb
```

To make the path known as a user in your system, you can do this either by editing the file `~/.profile` or the file `~/.bashrc` and adding this to your existing path variable.

Use your favorite editor and edit one of the two files.

```
vim ~/.bashrc
```

Add the following content in a new line at the end of the file.

```
export PATH="$PATH:~/bin"
``` 
So that the whole thing is also loaded in the system, you should now load the previously selected file `~/.bashrc` or `~/.profile` again. We do this with `source ~/.bashrc` or `source ~/.profile`

```
source ~/.bashrc
```

## Configure rweb

### config.yaml

The script is structured in such a way that it always searches for the configuration in the user directory under `~/.rweb/config.yaml` first, thus ensuring that only this file is loaded if it exists there. If the file does not exist in the user directory under `~/.rweb./config.yaml`, it checks whether there is a directory + the configuration file .rweb/config.yaml in the current directory, and if so, it is loaded accordingly. This has the advantage that you can now store a separate configuration for each directory. With the parameter -c the configuration can also be loaded from another directory, e.g. `-c /etc/rweb/config.yaml` or `-c myserver1.yaml` 

If no config.yaml file is found, the web server falls back to FALLBACK variables in the script. Unless you use the parameters corresponding to -L LISTEN, -p path, -P port, -i allowed_ips, -D dir, -S static_dir.

If you only need a few parameters, the program recognizes these and accesses the config.yaml accordingly if available (depending on availability/path) or accesses the FALLBACK variable again accordingly.

This makes the small web server absolutely modular.

To create a simple webserver configuration in YAML format you only need the option -G

```bash
rweb -G
```

```
The file '/home/myuser/rweb/.rweb/config.yaml' generated successfully.
```

For global user settings copy the directory to ~/.rweb/config.yaml

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

For example:

```
allowed_ips:
- 192.168.1.10
listen: 0.0.0.0
port: 8080
default_message: Hello World!
default_directory: /
html_path: /home/myuser/rweb/index.html
static_directory: /home/myuser/rweb/static
```

For example, you can determine which IP addresses you want to allow access to the web server.

Alternatively, you can also specify the config.yaml configuration as a parameter.

```bash
rweb -G -i 10.10.10.2 127.0.0.1 -L 10.0.0.1 -P 8080
```

rweb will now read your parameters and write them directly to the config.yaml file.

```
The file '/home/myuser/rweb/.rweb/config.yaml' already exists. Do you want to overwrite it? (Y/n): Y
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
usage: rweb [-h] [-p PATH] [-P PORT] [-i IPS [IPS ...]] [-L LISTEN] [-c CONFIG] [-G] [-D DIRECTORY] [-S STATIC_DIR] [-l]

Flask App to display an HTML file

options:
  -h, --help                              show this help message and exit
  -p PATH, --path PATH                    Path to the HTML file to display
  -P PORT, --port PORT                    Port to run the Flask server on
  -i IPS [IPS ...], --ips IPS [IPS ...]   List of allowed IP addresses
  -L LISTEN, --listen LISTEN              IP address to listen on (default: 0.0.0.0)
  -c CONFIG, --config CONFIG              Path to the config file
  -G, --generate-config                   Generate a config.yaml file with the current settings
  -D DIRECTORY, --directory DIRECTORY     Default directory to serve files from
  -S STATIC_DIR, --static-dir STATIC_DIR  Directory to serve static files from (e.g., images)
  -l, --list-config                       List the current config.yaml file content and exit
~~~
