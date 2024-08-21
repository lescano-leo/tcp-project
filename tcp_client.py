import socket
import os

HOST = '127.0.0.1'
PORT = 50000

def main():
    """Função principal que conecta ao servidor e gerencia a interação com o usuário."""
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT))
    msg = ''

    try:
        while msg != '3':
            msg = input('Escolha sua opção:\n1. Enviar mensagem\n2. Mostrar um Mario\n3. Encerrar conexão\n')
            if msg == '1':
                msg2 = str.encode(input('Informe sua mensagem:'))
            elif msg == '2':
                msg2 = str.encode('Mario')
            elif msg == '3':
                msg2 = str.encode('ENCERRAR')
                c.sendall(msg2)
                break
            else:
                msg2 = str.encode('Escolha alguma opção')

            c.sendall(msg2)

            try:
                data = c.recv(2048)
                if data:
                    print('Resposta do servidor: ', data.decode())
                else:
                    print("Conexão fechada pelo servidor.")
                    break
            except socket.error as e:
                print("Erro ao receber dados:", e)
                break

    except (socket.error, BrokenPipeError) as e:
        print(f"Erro na conexão: {e}")
    finally:
        c.close()
        os.system('clear')

if __name__ == "__main__":
    main()
