### Description

Sometimes my neighbour plugs off the socket, and after a while the server (laptop) shuts down. To detect this, we use `acpi` daemon, that executes `handler.sh` script on a power outage. Depending on the event, a telegram message is sent to the developers' chat, so that appropriate measures can be taken.

### Installation

```bash
# Install dependencies
sudo pip install --upgrade -r requirements.txt

# Set a link to the handler script
sudo ln -sf $(realpath handler.sh) /etc/acpi/handler.sh

# Change $SEND_MESSAGE variable if needed
# nano handler.sh

# Install acpid daemon
pacaur -S acpid
sudo systemctl enable --now acpid
```
