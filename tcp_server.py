import socket
import threading
from datetime import datetime
import signal
import sys

# Lista global para armazenar IPs dos clientes conectados
ListaIP = []

# Dicionário global para armazenar conexões dos clientes
connections = {}

HOST = '127.0.0.1'
PORT = 50000

# Flag para controlar o encerramento do servidor
shutdown_flag = threading.Event()

def save_ips_to_file():
    """Salva os IPs dos clientes conectados em um arquivo."""
    with open('ips_conectados.txt', 'w') as file:
        for ip in ListaIP:
            file.write(ip + '\n')

def log_message(message, addr):
    """Registra uma mensagem recebida ou enviada em um arquivo de log."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('conversas.log', 'a') as file:
        file.write(f'[{timestamp}] {addr}: {message}\n')

def handle_client(conn, addr):
    """Gerencia a comunicação com um cliente conectado."""
    print(f'Conectado a: {addr}')
    connections[addr] = conn  # Armazena a conexão

    while not shutdown_flag.is_set():
        try:
            data = conn.recv(2048)
            if not data:
                break

            mensagem = data.decode()

            # Registra a mensagem recebida
            log_message(f'Recebido: {mensagem}', addr)

            if mensagem == 'ListarIPS':
                conn.sendall(str.encode('ListarIPS não disponível para clientes.'))
            elif mensagem == 'Macaco':
                txt = '''\n
                           ⣠⣴⣶⣿⣶⢠⣾⣿⣿⣶⣦⣀
                        ⣠⣾⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣷⣄
                       ⣰⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⣀⡀⠀
                  ⡀⠤⠤⢤⣿⣿⣿⣿⣿⣿⣿⡏⠈⣿⣿⣿⣿⣿⣿⣿⣿⣍⣴⣶⣾⣵⡄
                 ⣬⣾⠿⢷⣮⣿⣿⡿⠛⠉⠉⠉⠉⠀⠀⠀⠈⠉⠙⢿⣿⣿⣿⣿⡇⠉⠉⡹
                 ⢉⠀⢀⢸⢿⣿⣿⠀⠠⡲⣶⠶⡆⠀⡶⢛⣉⡠⡂⠀⢿⣿⣿⡟⣡⠿⠎⠁
                 ⠑⠻⠳⣼⣿⣿⡄⠈⠘⠿⠓⠙⠀⠃⠚⠛⠁⠀⠀⢸⣿⣿⣿⡅⠊
                     ⠊⢽⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣿⣿⣿⡙⠃
                     ⢸⣿⣿⣿⡗⠀⠀⠐⠄⠔⠀⠀⠀⠀⢻⣿⣿⣟⢷
                     ⠘⢹⣿⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿⣿⣿⣿
                       ⣿⣿⣷⣦⣤⣤⣤⣤⠤⠔⣊⣿⣿⣿⣟⢿
                       ⡟⣿⣿⣷⡐⠶⠶⠶⠖⢻⣿⣿⣿⣿⣿⠀
                       ⠈⢿⠻⣿⣷⣶⣶⣶⣿⡏⠻⣿⠈⠻
                           ⠙⣿⣿⠀⠹⣿⡇⠀⠋
                            ⠈⠻⡆⠀⠹⠁⠀'''
                conn.sendall(str.encode(txt))
            elif mensagem == 'ENCERRAR':
                conn.sendall(str.encode('Você está desconectado.'))
                break
            else:
                conn.sendall(data)

            # Registra a mensagem enviada
            log_message(f'Enviado: {mensagem}', addr)

        except ConnectionResetError:
            break
        except OSError:
            # Ignora erros se o socket já foi fechado
            break

    print(f'Conexão encerrada: {addr}')
    conn.close()
    del connections[addr]  # Remove a conexão quando o cliente desconecta
    #ListaIP.remove(addr[0])  # Remove o IP da lista
    save_ips_to_file()  # Salva a lista atualizada de IPs em um arquivo

def shutdown_server(signal, frame):
    """Encerramento gracioso do servidor quando sinal de interrupção (Ctrl+C) é recebido."""
    print('\nDesligando o servidor...')
    shutdown_flag.set()
    for conn in list(connections.values()):
        try:
            conn.sendall(str.encode('O servidor está encerrando.'))
        except OSError:
            pass
        finally:
            conn.close()
    save_ips_to_file()
    sys.exit(0)

def main():
    """Função principal que inicializa o servidor e aceita conexões de clientes."""
    signal.signal(signal.SIGINT, shutdown_server)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print('Servidor ativo. Aguardando conexões...')

    while not shutdown_flag.is_set():
        try:
            conn, addr = s.accept()
            if shutdown_flag.is_set():
                conn.close()
                break
            print(f'Nova conexão de {addr}')
            if addr[0] not in ListaIP:
                ListaIP.append(addr[0])

            # Inicia uma nova thread para cada cliente
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

        except OSError:
            # Ignora erros se o socket já foi fechado
            break

    s.close()

if __name__ == "__main__":
    main()
