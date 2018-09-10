cd /net/pek-simics1/opt/shared/yun
./pyenv.init
cd lem
/net/pek-simics1/opt/shared/yun/.pyenv/versions/3.4.0/bin/python3 lemserver --host 128.224.166.211  --port 9090  --log-host-ip pek-hv-portal  --log-host-port 27017  --log-database lemdata   --log-host-user lem  --log-host-password lem-m4n4g3r > /dev/null 2>&1 &

