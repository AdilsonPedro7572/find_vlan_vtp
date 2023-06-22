from netmiko import ConnectHandler
from tabulate import tabulate
from segredos import nome,senha,ips_list
# Lista de IPs dos dispositivos
ips = ips_list

# Dados de autenticação
username = nome
password = senha

# VLAN a ser verificada
vlan = input('Digite o número da VLAN: ')

# Lista para armazenar os resultados
resultados = []

# Loop através dos IPs
for ip in ips:
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
    }

    try:
        # Conexão SSH ao dispositivo
        net_connect = ConnectHandler(**device)

         # Enviar comando para verificar o modo VTP
        output_vtp = net_connect.send_command('show vtp status | include VTP Operating Mode')
        
        # Extrair o modo VTP do resultado
        mode = output_vtp.split(":")[1].strip()

        # Enviar comando para listar VLANs
        output_vlan = net_connect.send_command('show vlan brief')

        # Verificar se a VLAN está presente na saída
        vlan_presente = 'Sim' if vlan in output_vlan else 'Não'
 

        # Armazenar os resultados na lista
        resultados.append([ip, mode, vlan_presente])

        # Fechar a conexão SSH
        net_connect.disconnect()

    except Exception as e:
        print(f'Erro ao conectar ao dispositivo {ip}: {str(e)}')

# Exibir os resultados em forma de tabela
headers = ['Endereço IP', 'Modo VTP', f'VLAN Presente[{vlan}]']
print(tabulate(resultados, headers=headers))