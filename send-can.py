import can
import time

def parse_can_message(line):
    # Remove os parênteses e divida a linha por espaços
    parts = line.strip().split()
    timestamp = float(parts[0][1:-1])
    can_interface = parts[1]
    can_id_data = parts[2].split('#')
    can_id = int(can_id_data[0], 16)
    data = bytes.fromhex(can_id_data[1])
    flag = parts[3]
    return timestamp, can_interface, can_id, data, flag

def send_can_messages(file_path, interface):
    # Configurar a interface CAN
  with can.interface.Bus(channel=interface, bustype='socketcan') as bus:

    with open(file_path, 'r') as f:
      for line in f:
        timestamp, can_interface, can_id, data, flag = parse_can_message(line)
        message = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
        try:
          flag = "NORMAL" if flag == 'R' else "ATAQUE"
          bus.send(message)
          print(f"Message sent on {can_interface}: {message} LABEL = {flag}")
        except can.CanError:
          print("Message NOT sent")
        time.sleep(0.5)
if __name__ == "__main__":
    file_path = 'IMPERSONATION_ATCK.txt'  # Substitua pelo caminho do seu arquivo de mensagens
    interface = 'can0'  

    send_can_messages(file_path, interface)
