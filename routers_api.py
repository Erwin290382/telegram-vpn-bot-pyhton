from routeros_api import RouterOsApiPool

# Konfigurasi login Mikrotik
HOST = 'ISI DENGAN IP MIKROTIK'       # Ganti sesuai IP Mikrotik kamu
USERNAME = 'api_user'        # Username API kamu
PASSWORD = 'api12345'        # Password API kamu
PORT = 8728                  # Port API Mikrotik

# Profile VPN dan IP Pool
VPN_PROFILE = 'VPN PROFILE'              # Sesuaikan dengan profil di Mikrotik
VPN_REMOTE_POOL = 'VPN-POOL'             # Sesuaikan dengan IP Pool yang ada
SERVICE = 'l2tp'

# Fungsi membuat user VPN dan NAT rule
def create_vpn_user(username, password, port):
    try:
        api_pool = RouterOsApiPool(
            HOST, username=USERNAME, password=PASSWORD, port=PORT, plaintext_login=True
        )
        api = api_pool.get_api()

        # Tambah PPP Secret (L2TP user)
        api.get_resource('/ppp/secret').add(
            name=username,
            password=password,
            service=SERVICE,
            profile=VPN_PROFILE
          
        )

        # Tambah NAT rule agar Winbox bisa diakses via port custom
        api.get_resource('/ip/firewall/nat').add(
            chain='dstnat',
            action='dst-nat',
            to_ports='8291',
            protocol='tcp',
            dst_port=str(port),
            in_interface='ether1',
            to_addresses='192.168.10.2'  # Ganti sesuai IP lokal Mikrotik kamu
        )

        api_pool.disconnect()
        return True

    except Exception as e:
        print('[API Error]', e)
        return False

# Fungsi hapus user VPN dan NAT rule
def delete_vpn_user(username, port):
    try:
        api_pool = RouterOsApiPool(
            HOST, username=USERNAME, password=PASSWORD, port=PORT, plaintext_login=True
        )
        api = api_pool.get_api()

        # Hapus user dari PPP Secret
        ppp_resource = api.get_resource('/ppp/secret')
        for user in ppp_resource.get():
            if user['name'] == username:
                ppp_resource.remove(id=user['.id'])
                break

        # Hapus rule NAT berdasarkan dst-port
        nat_resource = api.get_resource('/ip/firewall/nat')
        for rule in nat_resource.get():
            if rule.get('dst-port') == str(port):
                nat_resource.remove(id=rule['.id'])
                break

        api_pool.disconnect()
        return True

    except Exception as e:
        print('[API Error]', e)
        return False
