from can import Message
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


def read_from_can():
  interface = 'socketcan'
  channel = 'can0'
  naoDetectados=[]
  try:

      while True:
        with can.Bus(interface=interface,channel=channel) as bus:
          message = bus.recv()
          if(filtro_DBC(message)):
            print("ATAQUE DETECTADO!\n")
          else:
      #tratar o dado pra entrada do modelo
#      id=message.arbitration_id
 #     dlc=message.dlc
  #    data=[int(message.data[i], 16) for i in range(0, len(message.data))] #message.data    do tipo bytes j   separado em bytes!!!
   #   data += [0] * (8 - len(data))
    #  naoDetectados.append([id,dlc]+ data) #ou model.predict( ([id,dlc]+ data) ) considerando a entrada do modelo um array
      #nessa linha desse comentario, seria verificado a predi    o do modelo, que responderia pra ataque ou n  o        print("MENSAGEM NORMAL")
            print("MENSAGEM NORMAL\n")
            print(int.from_bytes(message.data, byteorder='big'))
  #aqui na pratica n sei oq daria pra p  r
 # df = pd.DataFrame(sequences,columns=['can_id','can_dlc','data0','data1','data2','data3','data4','data5','data6','data7'])
  #df = codificar_dados(df) #o retorno daqui ta pronto pro 'predict' do modelo. e aqui tem 10 mensagens
 # return df
  except KeyboardInterrupt:
    print("\n Interrupted by user. Exiting...")
  finally:
    bus.shutdown()
read_from_can()