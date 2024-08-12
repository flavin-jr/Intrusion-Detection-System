
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
from can import Message
import joblib
import can
def test_index(mensagem):
  can_message_map=[0x007,0x008,0x00D,0x00E,0x014,0x015,0x016,0x017,0x041,0x055,0x056,0x05B,0x05C,0x05D]
  try:
    index=can_message_map.index(mensagem.arbitration_id)
    return index
  except:
    return -1


def filtro_DBC(mensagem): #retorna True se for ataque direto. Se n  o, retorna False
  can_message_map_dlc=[1,1,2,2,1,1,1,1,1,1,1,2,4,1]
  if(test_index(mensagem)==-1):#Se a mensagem nao tiver um indice relacionado,    ataque
    return True
  elif can_message_map_dlc[test_index(mensagem)]!=mensagem.dlc:
      return True
  else:
    return False

def process_can_msg(message):
  processed_msg = []
  id=message.arbitration_id
  dlc=message.dlc
  data=[message.data[i] for i in range(0, dlc)] #message.data    do tipo bytes j   separado em bytes!!!
  data += [0] * (8 - len(data))
  processed_msg.append(id)
  processed_msg.extend(data)
  return processed_msg

def read_from_can():
  interface = 'socketcan'
  channel = 'can0'
  try:

      model = joblib.load('random_forest_classifier.pkl')
      while True:
        with can.Bus(interface=interface,channel=channel) as bus:
          message = bus.recv()
          if(filtro_DBC(message)):
            print("ATAQUE DETECTADO!\n")
          else:
          #tratamento de dados para o modelo
            processed_msg = process_can_msg(message)
            result = model.predict([processed_msg])
            result = "MENSAGEM NORMAL\n" if result[0]==0 else "ATAQUE DETECTADO!\n"
            print(result)


  except KeyboardInterrupt:
    print("\n Interrupted by user. Exiting...")
  finally:
    bus.shutdown()
read_from_can()