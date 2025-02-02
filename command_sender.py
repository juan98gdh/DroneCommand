import argparse
import socket
import string

descripcion = """Envia un comando a un componente de la UREJ.
\n
Por ejemplo, para enviar un comando LINK a drone que corre en la dirección IP 127.0.0.1\n
y puerto 50001, se debe ejecutar algo similar a lo siguiente:\n
# python3 command_sender.py --host 127.0.0.1:50001 "{'msg_type' = 'LINK', 'et_id' = 5}"\n
suponiendo un formato de mensaje basado en JSON.
"""

#
# FUNCIÓN: init_argparse
# ARGS: Ninguno
# DEVUELVE: Objeto ArgumentParser conteniendo los argumentos leidos de la
# línea de comandos
# DESCRIPCIÓN: Parsea los argumentos proporcionados por el usuarios


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPCIONES] [MENSAJE]...",
        description=descripcion,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--host", action="store",
                        help="Dirección IP:puerto del componente")
    parser.add_argument("--no_response", action="store_true",
                        help="No espera por una respuesta (ACK)")
    parser.add_argument('mensaje', nargs='*', type=str,
                        help="Tipo de mensaje (LINK, FLY, etc.)")
    return parser


def main() -> None:
    # Parseamos los argumentos de la línea de comandos
    parser = init_argparse()
    args = parser.parse_args()

    # Parseamos los argumentos de la línea de comandos
    if not args.mensaje:
        print("ERROR: Debes proporcionar un tipo de mensaje a enviar")
    else:
        # Preparamos la cadena para ser enviada
        mensaje = args.mensaje[0].encode()
        # Separamos el host y el puerto
        host, puerto = args.host.split(':')

        # Confiamos en que el usuario sepa lo que hace y el mensaje
        # esté bien formateado... :)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(host, puerto, mensaje)
            s.connect((host, int(puerto)))
            s.sendall(mensaje)
            # Se espera algún tipo de ACK por parte del elemento
            if not args.no_response:
                data_ack = s.recv(1024)
                print(data_ack)


if __name__ == "__main__":
    main()
