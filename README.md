# stalkerware-urls

List of DNS entries that stalkerware uses to communicate with their C2C servers.

philez

```
Stalkerware_subdomains.txt - list of subdomains in a newline formated, original

shove_it_in_your_pi-hole.py - python script for converting the above txt file
into something your pi-hole can use. Cleans with the power of snark. see --help
for more info

stalkerware_subdomains.pi_hole - proccessed list that can be fed directly into
a pi-hole to block stalkerware domains.(or at least interrupt with their DNS)

```

Pi-hole: https://github.com/pi-hole/pi-hole

Is a DNS server designed for raspberry pis or low power computers that blocks
Advertisements automaticly. Once you have pi-hole running, you may add this
under "Group Management" -> "Adlists". add the following as the URL:

```
https://raw.githubusercontent.com/GIJack/stalkerware-urls/shove_it_in_your_pi-hole/stalkerware_subdomains.pi_hole
```
if you forked this, substitute "GIJack" with your github username.

Maintain the proccessed list, everytime you make a change

```
/shove\_it\_in\_your\_pi-hole.py stalkerware\_subdomains.txt -o stalkerware\_subdomains.pi\_hole
```
