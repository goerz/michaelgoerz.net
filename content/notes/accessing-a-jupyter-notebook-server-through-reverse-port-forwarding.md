---
Date: 2016-12-22 10:51:27
Modified: 2017-10-31 17:00:00
Category: Tech
Tags: computation, jupyter, ssh, python
---

# Accessing a Jupyter notebook server through reverse port forwarding

So you’re running a [jupyter notebook][1] on some remote workstation (let's
say `myworkstation.stanford.edu`) that's firewalled and only allows access via
SSH. The notebook server runs on e.g. port 8888.

## SSH Port Forwarding ##

To connect to the server from your laptop, you could use SSH port forwarding:

    laptop:~> ssh -L 8888:localhost:8888 myworkstation.stanford.edu

You then point the browser on your laptop to `http://localhost:8888` to access
the notebook.


## Reverse Port Forwarding ##

What, however, if you do this from an iPad, or a locked down Windows computer
that doesn't have SSH or the ability for port forwarding? In this case, you can
still get through the firewall around `myworkstation` by using *reverse* port
forwarding via another non-firewalled (web-)server (the "forwarding server").
Note that exposing a standard notebook server directly is *not* a good solution
for sharing notebooks among a larger group of people on a regular basis. That
is something that [jupyterhub][2] is designed to solve.

Whenever you expose a jupyter notebook server to the internet,
security is a major concern! Anybody who gets access to your notebook server
gets a full shell on `myworkstation`. Therefore, we must

1. [Set a strong password for the notebook server][3]
2. Use SSL to encrypt the connection. A self-signed certificate will not be
   sufficient in our case, so we'll use [letsencrypt][4] to get a proper (free)
   certificate.  If SSL is not configured correctly, only connections between
   the forwarding server and `myworkstation` will be encrypted (via SSH), while the
   connection between the laptop/iPad and the forwarding server is completely open,
   making it easy to break into `myworkstation`.

To set up the forwarding server, I'm assuming you have a `server` with root
access, and a domain name. I will be using the [Digital Ocean][5] server that
handles my website (`michaelgoerz.net`). We need the following configuration
steps:

1.  Set up a subdomain in the DNS for the domain, e.g.
    `jupyter.michaelgoerz.net` (pointing to the IP of `server`). If you're
    using something like [Cloudflare][6], the subdomain must *not* go through
    their proxy.

2.  Create a new letsencrypt SSL Key for the subdomain: temporarily disable any
    running webserver (making port 80 available for the letsencrypt
    authorization procedure), then run e.g.

        server:~> sudo /opt/letsencrypt/certbot-auto certonly –standalone -d jupyter.michaelgoerz.net

    This does not conflict with the existing certificate for
    `michaelgoerz.net`/`www.michaelgoerz.net` (and having separate keys from my
    normal website is the entire reason for having set up the `jupyter` subdomain).
    The new certificate files end up in
    `/etc/letsencrypt/live/jupyter.michaelgoerz.net`.

3.  Configure `sshd` on `server` to expose reverse-forwarded ports to the internet.
    In `/etc/ssh/sshd_config`, set

        GatewayPorts clientspecified

    Restart the ssh server with `service ssh restart`.

Now we can run the jupyter notebook server on `myworkstation`. The certificate
files `/etc/letsencrypt/live/jupyter.michaelgoerz.net/privkey.pem` and
`/etc/letsencrypt/live/jupyter.michaelgoerz.net/cert.pem` need to be copied to
some accessible location on `myworkstation`, e.g. to
`~/jupyter.michaelgoerz.net.privkey.pem` and
`~/jupyter.michaelgoerz.net.cert.pem`,
respectively.

The following command tells the jupyter notebook server to use the key files:

    myworkstation:~> jupyter notebook --certfile=$HOME/jupyter.michaelgoerz.net.cert.pem --keyfile=$HOME/jupyter.michaelgoerz.net.privkey.pem

Note that you can also set this up permanently in
`~/.jupyter/jupyter_notebook_config.py`, but since I will only do the
forwarding sporadically, I prefer to have it as a command line option on a
case-by-case basis.

Lastly, on `myworkstation`, we make the reverse port forwarding connection to
`server`:

    myworkstation:~> ssh server -N -R :8888:localhost:8888

This command must run for as long as we want the notebook server to be
accessible.

You could also use the `-f` option to put this in the background. Note the
leading colon in `:8888:localhost:8888`. This works in conjunction with
`GateWayPorts clientspecified` to ensure that the remote socket listens on all
network interfaces, i.e. it will be available via the `server` public IP, not
just via `localhost`. [One could also set `GateWayPorts` to `yes` and leave out
the leading colon, but the configuration here is much more secure.][7]

The jupyter notebook server will now be accessible from the internet at large at
`https://jupyter.michaelgoerz.net:8888`.

## Reverse Proxying through Nginx ##

An alternative to the above procedure is to use `nginx` proxying. This assumes
that there is an `nginx` webserver running on `server`. The basic idea is this:
We start the jupyter notebook on `myworkstation`, without SSL encryption (but
with password protection!). Then, we create a tunnel from `server` to
`myworkstation`.

    server:~> ssh -N -L 8888:localhost:8888 myworkstation.stanford.edu

This would make the notebook locally accessible on `server` (but does not
expose it to the internet at large). The last step is to configure `nginx` to
act as a proxy to the locally forwarded port, expose it to the internet, and
wrap it in SSL. In the appropriate config file
(`/etc/nginx/sites-available"/default`, in my case), I've added a section

    server {
        listen 443 ssl;
        server_name jupyter.michaelgoerz.net;
        ssl_certificate /etc/letsencrypt/live/jupyter.michaelgoerz.net/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/jupyter.michaelgoerz.net/privkey.pem;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        ssl_dhparam /etc/ssl/certs/dhparam.pem;
        ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_stapling on;
        ssl_stapling_verify on;
        add_header Strict-Transport-Security max-age=15768000;
        client_max_body_size 0;
        location / {
            proxy_pass http://127.0.0.1:8888/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }

This uses the same certificate files that were created above. Now, upon
restarting the webserver (`service nginx restart`), the notebook server is
publicly available at `https://jupyter.michaelgoerz.net`. The connection between
the browser and `server` is SSL-encrypted, and the connection from `server` to
`myworkstation` is encrypted through SSH. The `proxy_set_header` settings are
required to properly forward the websocket connections that the notebook relies
on.

The approach has several advantages compared to reverse-forwarding:

*   SSL keys stay on `server`. Instead of generating a separate key for for
    `jupyter.michaelgoerz.net`, you may just add the `jupyter` subdomain to the
     main key that the webserver uses anyway.
*   No need to configure `sshd` on `server` to expose reverse-forwarded ports
*   No need to configure SSL for the jupyter notebook server
*   The port number of the jupyter server will not be exposed.

The two drawbacks are:

*   Need to have `nginx` server running on `server`
*   Need to interact both with `myworkstation` (to start the notebook server)
    and with `server` (to initiate the port-forwarding SSH connection)

[1]: http://jupyter.org
[2]: https://jupyterhub.readthedocs.io/en/latest/
[3]: http://jupyter-notebook.readthedocs.io/en/latest/public_server.html#notebook-server-security
[4]: https://letsencrypt.org
[5]: http://digitalocean.com
[6]: http://cloudflare.com
[7]: http://askubuntu.com/questions/50064/reverse-port-tunnelling
