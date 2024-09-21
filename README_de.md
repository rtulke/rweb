# rweb
Ein einfacher Webserver für einzelne HTML-Seiten

`rweb` (Roberts WebServer), ist eine einfache Flask-Anwendung, die es erlaubt, eine einzelne HTML-Datei anzuzeigen, die über eine YAML-Konfigurationsdatei oder Kommandozeilenargumente konfiguriert wird. Bei der Entwicklung einiger meiner kleineren Projekte brauchte ich eine schnelle Möglichkeit, einen einfachen Webserver zu konfigurieren, der nicht mehr kann als eine einfache HTML-Datei anzuzeigen.

Der Server-Port, die erlaubten IP-Adressen, der HTML-Dateipfad, die "lauschende" IP-Adresse, sowie das einschalten von Logging und der Standard-HTML-Inhalt können über `config.yaml` konfiguriert werden. Wenn ein Kommandozeilenargument angegeben wird, überschreibt es die entsprechende Einstellung in der `config.yaml`. Wenn weder eine Konfigurationsdatei noch Argumente angegeben werden, greift das Skript auf Standardvariablen zurück. Eine Konfigurationsdatei kann mit der Option `--generate-config` (`-G`) erzeugt werden.


## Setup


### Einrichten einer Entwicklungsumgebung 

#### Git Installation

```
sudo apt update && apt upgrade
sudo apt install -y git
```

#### Git Konfiguration (optional)
Wenn Du deine Änderungen für das rweb-Projekt über git einchecken möchtest, solltest Du auch deinen Namen und E-Mail-Adresse für git angeben.

```
git config --global user.name "Your Name"
git config --global user.email "your@email-address.com"
```

### Setup rweb

#### Installation der erforderlichen Python3-Module

Es gibt einige Module, die zusätzlich installiert werden müssen. Die meisten anderen von rweb verwendeten Module sollten bereits durch die Python-Installation eingerichtet worden sein.

```
pip3 install flask yaml
```

```
mkdir -p ~/dev/
cd ~/dev/
git clone https://github.com/rtulke/rweb.git
```

Wir haben nun rweb heruntergeladen und es befindet sich im Verzeichnis ~/dev unterhalb Ihres Benutzerverzeichnisses. Wenn Sie rweb als Befehl ausführen wollen, sollten Sie die folgenden Anpassungen vornehmen. Ansonsten müssten Sie immer `python3 rweb.py <param> <arg>.` schreiben.


```
mkdir -p ~/bin/
cd ~/dev/rweb
cp rweb.py ~/bin/rweb
chmod +x ~/bin/rweb
```

Um den Pfad als Benutzer in deinem System bekannt zu machen, kannst Du entweder die Datei `~/.profile` oder die Datei `~/.bashrc` bearbeiten und diese zu deiner bestehenden Pfadvariable hinzufügen.

Verwende deinen bevorzugten Editor und bearbeite eine der beiden Dateien.

```
vim ~/.bashrc
```

Füge den folgenden Inhalt am Ende der Datei `~/.bashrc` ein.

```
export PATH="$PATH:~/bin"
``` 
Damit das Ganze auch im System geladen wird, sollten Sie nun die zuvor ausgewählte Datei `~/.bashrc` oder `~/.profile` erneut laden. Dies tun wir mit `source ~/.bashrc` oder `source ~/.profile`.

```
source ~/.bashrc
```

## rweb Konfigurieren

### config.yaml

Das Skript ist so aufgebaut, dass es immer zuerst im Benutzerverzeichnis unter `~/.rweb/config.yaml` nach der Konfiguration sucht und damit sicherstellt, dass nur diese Datei geladen wird, wenn sie dort existiert. 

Ist die Datei nicht Benutzerverzeichnis unter `~/.rweb./config.yaml`  vorhanden, wird geprüft, ob es im aktuellen Verzeichnis ein Verzeichnis also auch die Konfigurationsdatei .rweb/config.yaml gibt, wenn ja, wird diese entsprechend geladen. Dies hat den Vorteil, dass man nun für jedes Verzeichnis eine eigene Konfiguration speichern kann. 

Mit dem Parameter -c kann die Konfiguration auch aus einem anderen Verzeichnis geladen werden, z.B. `-c /etc/rweb/config.yaml` oder `-c myserver1.yaml` Somit wäre es möglich mehrere Webserver gleichzeitig laufen zu lassen die Ihre Konfiguration aus der `config.yaml` Datei beziehen.

Wenn keine config.yaml-Datei gefunden wurde, greift der Webserver auf die FALLBACK-Variablen im Skript zurück. Es sei denn, Du verwendest die Parameter entsprechend `-L LISTEN`, `-p path`, `-P port`, `-i allowed_ips`, `-D dir`, `-S static_dir`.

Benötigt man nur wenige Parameter, erkennt das Programm diese und greift entsprechend auf die config.yaml zu, falls vorhanden (je nach Verfügbarkeit und Pfad) andernfalls greift `rweb` entsprechend wieder auf die FALLBACK-Variable zurück.

Das macht den kleinen Webserver absolut modular.

Um eine einfache Webserver-Konfiguration im YAML-Format zu erstellen, benötigst Du lediglich die Option -G.

```bash
rweb -G
```

```
The file '/home/myuser/rweb/.rweb/config.yaml' generated successfully.
```

Für globale Benutzereinstellungen kopieren Sie das Verzeichnis nach `~/.rweb/config.yaml`

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

Du könntest nun die config.yaml selbst bearbeiten und weitere Anpassungen vornehmen.

```bash
vim config.yaml
```

Als Beispiel:

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

So könnte man beispielsweise festlegen, welche IP-Adressen für den Zugriff auf den Webserver zulassen werden sollen.

Alternativ dazu kann mann auch die config.yaml-Konfiguration als Parameter angeben. In Kombination mit dem Parameter -G werden die weiteren Parameter und Argumente direkt in die Konfigurationsdatei geschrieben.

```bash
rweb -G -i 10.10.10.2 127.0.0.1 -L 10.0.0.1 -P 8080
```

`rweb` liest nun die Parameter und schreibt diese direkt in die Datei config.yaml.

```
The file '/home/myuser/rweb/.rweb/config.yaml' already exists. Do you want to overwrite it? (Y/n): Y
Config file 'config.yaml' generated successfully.
```

```bash
cat config.yaml
```

Wie man sehen kann, wurden nur die Dinge angepasst, die als Parameter übergeben wurden. Die zuvor erstellte Konfiguration bleibt unangetastet.

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

Wenn der Parameter `-G` weggelassen wird, werden die Parameter als Starteingabe interpretiert und der Webserver startet mit den angegebenen Parametern.

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

## Befehle & Argumente, eine Übersicht

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
