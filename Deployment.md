# Deployment einer Webanwendung

## Deckblatt

## Inhaltsverzeichnis

## Vorgehen

### Netzwerkkonfiguration

#### Statische IP Festlegen

Zuerst die Datei /etc/dhcpcd.conf wie folgt editieren um eine statische IP zu erhalten 
````
#static IP configuration LAN
interface eth0
static ip_address=192.168.24.134/24
static routers=192.168.24.254
static domain_name_servers=192.168.24.254

#static IP configuration WLAN
interface wlan0
static ip_address=192.168.24.164/24
static routers=192.168.24.254
static domain_name_servers=192.168.24.254
````
Anschließend den Daemon mit neustarten
````
sudo systemctl restart dhcpcd
````

Für WLAN die Datei /etc/wpa_supplicant/wpa_supplicant.conf editieren
````
ctrl_interface=DIR=/var/run/wpa_supplicant 
GROUP=netdev
country=de
update_config=1
network={
    ssid="r324-public"
    psk="aehUa6ye"
}
````
Anschließen den Service neustarten
````
sudo systemctl restart dhcpcd
````

Verfügbare Netzwerke anzeigen
````
wpa_cli -i wlan0 list_networks
````

Falls kein Netzwerk angezeigt wird, Netzwerk einrichten
In das CLI gehen mit wpa_cli

````
scan
scan_results
add_network
add_network 0 ssid "SSID"
add_network 0 psk "passphrase"
enable_network 0
save_config
quit
````

Nun kan man sich im WLAN anmelden
````
wpa_cli -i wlan0 select_network 0 
````

### Benutzer anlegen und konfigurieren
````
sudo adduser benutzer72
sudo adduser fernzugriff
````

Fernzugriff soll sudo Rechte bekommen also wird er zur sudo group hinzugefügt
````
sudo adduser fernzugriff sudo
````

### Firewall konfiguration
Zuerst Firewall installieren
````
sudo apt-get install ufw
````

Firewall Regeln festlegen
````
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
````

Firewall aktivieren
````
sudo ufw enable
````

### ToDo-Listen-Verwaltung deployen

Git, Docker und Docker Compose installieren
````
sudo apt-get install git
````

### Nextcloud Filehosting als Docker Container 