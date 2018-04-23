```bash
# Install dependencies
sudo pip install --upgrade -r requirements.txt

# Install acpid daemon
pacaur -S acpid
sudo systemctl enable --now acpid

# Set a link to the handler script
sudo ln -sf $(realpath handler.sh) /etc/acpi/handler.sh
```
