def ler_automato(arquivo):
  """
  Lê o arquivo de representação do autômato finito e retorna um dicionário com as informações do autômato.

  Argumentos:
    arquivo (str): Caminho para o arquivo de texto com a representação do autômato.

  Retorna:
    dict: Dicionário contendo as informações do autômato:
      * estados: Conjunto de estados do autômato.
      * alfabeto: Conjunto de símbolos do alfabeto.
      * transicao: Dicionário que representa a função de transição, onde cada chave é um par (estado, símbolo) e o valor é o próximo estado.
      * estado_inicial: Estado inicial do autômato.
      * estados_finais: Conjunto de estados finais do autômato.
  """
  estados = set()
  alfabeto = set()
  transicao = {}
  estado_inicial = None
  estados_finais = set()

  with open(arquivo, 'r') as f:
    for linha in f:
      linha = linha.strip()
      if not linha:
        continue

      # Separa os campos da linha
      campos = linha.split()

      if campos[0] == 'estados':
        estados = set(campos[1:])
      elif campos[0] == 'alfabeto':
        alfabeto = set(campos[1:])
      elif campos[0] == 'transicao':
        for i in range(1, len(campos), 3):
          origem = campos[i]
          simbolo = campos[i + 1]
          destino = campos[i + 2]

          if origem not in transicao:
            transicao[origem] = {}
          transicao[origem][simbolo] = destino
      elif campos[0] == 'estado_inicial':
        estado_inicial = campos[1]
      elif campos[0] == 'estados_finais':
        estados_finais = set(campos[1:])
      else:
        raise ValueError(f"Linha inválida no arquivo de autômato: {linha}")

  # Validação das informações do autômato
  if not estado_inicial:
    raise ValueError("Estado inicial não definido no arquivo de autômato.")

  if estado_inicial not in estados:
    raise ValueError(f"Estado inicial '{estado_inicial}' não pertence aos estados do autômato.")

  if not estados_finais:
    raise ValueError("Nenhum estado final definido no arquivo de autômato.")

  for origem, destinos in transicao.items():
    if origem not in estados:
      raise ValueError(f"Estado de origem '{origem}' na função de transição não pertence aos estados do autômato.")

    for simbolo in destinos:
      if simbolo not in alfabeto:
        raise ValueError(f"Símbolo '{simbolo}' na função de transição não pertence ao alfabeto do autômato.")

      if destinos[simbolo] not in estados:
        raise ValueError(f"Estado de destino '{destinos[simbolo]}' na função de transição não pertence aos estados do autômato.")

  return {
      'estados': estados,
      'alfabeto': alfabeto,
      'transicao': transicao,
      'estado_inicial': estado_inicial,
      'estados_finais': estados_finais,
  }

def simular_cadeia(automato, cadeia):
  """
  Simula o autômato finito com a cadeia de entrada fornecida e retorna o estado final alcançado.

  Argumentos:
    automato (dict): Dicionário contendo as informações do autômato.
    cadeia (str): Cadeia de entrada a ser processada.

  Retorna:
    str: Estado final alcançado pela simulação.
  """
  estado_atual = automato['estado_inicial']

  for simbolo in cadeia:
    if simbolo not in automato['alfabeto']:
      raise ValueError(f"Símbolo '{simbolo}' não pertence ao alfabeto do autômato.")

    if estado_atual not in automato['transicao'] or simbolo not in automato['transicao'][estado_atual]:
      return None  # Cadeia rejeitada (transição indefinida)

    estado_atual = automato['transicao'][estado_atual][simbolo]

  return estado_atual

def processar_testes(automato, arquivo_entrada, arquivo_