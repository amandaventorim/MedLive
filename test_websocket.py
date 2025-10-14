#!/usr/bin/env python3
"""
Script de teste para verificar se o WebSocket de vídeo está funcionando
"""

import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/video/test_room/medico/1"
    
    try:
        print(f"Tentando conectar em: {uri}")
        async with websockets.connect(uri) as websocket:
            print("✅ Conexão WebSocket estabelecida com sucesso!")
            
            # Enviar uma mensagem de teste
            test_message = {
                "type": "test",
                "message": "Hello from test script"
            }
            
            await websocket.send(json.dumps(test_message))
            print("✅ Mensagem enviada")
            
            # Aguardar resposta por 2 segundos
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                print(f"✅ Resposta recebida: {response}")
            except asyncio.TimeoutError:
                print("⚠️ Timeout aguardando resposta (isso é normal)")
                
    except Exception as e:
        print(f"❌ Erro na conexão WebSocket: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== TESTE DE WEBSOCKET DE VÍDEO ===")
    print("Certifique-se de que o servidor está rodando em http://127.0.0.1:8000")
    print()
    
    result = asyncio.run(test_websocket())
    
    if result:
        print("\n✅ Teste concluído com sucesso!")
    else:
        print("\n❌ Teste falhou!")
