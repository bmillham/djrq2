Adding a new DJ.

1) Add DNS record on Digital Ocean (CNAME record pointing to rockitradio.space)
2) Update bin/createcert.sh with new DJs DNS
 2a) Run createcert.sh
 2b) Select (E)xpand)
 2c) Select 1 (No Redirect)
3) Add an new record in database djrq2 table update_options for the DJ and create the empty database
 3a) cd djrq2
 3b) . bin/activate # Start the VENV
 3c) cd djrq2/tools
 3d) python add_new_dj.py --dj NewDJName --passwd djspassword -u mysqlusername -P mysqlpassword -s ip/servername_of_mysql_server prokyon
 3e) Restart djrq
     i) sudo systemctl restart djrq
4) Create the private area (optional, it will be created automatically when the user first accesses it)
 4a) mkdir ~/djrq2/privatefilearea/DJName # case sensitive!

