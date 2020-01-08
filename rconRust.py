# -*- coding: utf-8 -*-
"""
@author: jsmeele
"""

import asyncio
import websockets

class RCONClient:

    def __init__(self):
        self.HOST           = 'xx.xx.xx.xx'     # IP/URL
        self.PORT           = 28016             # Port to listen on
        self.PASS           = 'password'        # Password
        self.__BANLIST      = '{"identifier":1000,"message":"banlist"}'
        self.__PLAYERLIST   = '{"identifier":2000,"message":"playerlist"}'
        self.__URI          = 'ws://%s:%s/%s' % (self.HOST,self.PORT,self.PASS)
        self.__CONNECTION   = None
        self.__LOOP         = asyncio.get_event_loop()
        self.__TASK         = None

    async def connect(self):
        # Connection to WebSocket
        self.__CONNECTION = await websockets.connect(self.__URI, ping_interval=None)
        
        if self.__CONNECTION.open:
            print('Connection established.')
            # start the receiveMessage coroutines and coexist in Task wrappers
            self.__TASK = asyncio.ensure_future(self.receiveMessage())
            await self.__TASK
            print('END')
    
    async def close(self):
        self.__TASK.cancel()
            
        await self.__CONNECTION.close()
        print('Connection with server closed')
    
    async def receiveMessage(self):
        # Receiving all server messages and handling them
        while True:
            try:
                message = await self.__CONNECTION.recv()
                print('Received message from server: ' + str(message))
            except websockets.exceptions.ConnectionClosedError:
                print('Connection Closed Error')
                break

    async def sendMessage(self, message):
        # Sending message to webSocket server
        print('Send Message.')
        await self.__CONNECTION.send(message)
    
    def run(self):
        if self.__LOOP.is_running():
            asyncio.gather(self.connect())
        else:
            print('Event Loop Not Running')
      
        
if __name__ == '__main__':
    # Application object
    client = RCONClient()
    
    # Start Application
    client.run()
