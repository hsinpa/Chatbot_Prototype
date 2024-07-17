import { createContext, useEffect, useState } from 'react'
import { Header_Comp } from './layout/header'
import { User_Text_Input } from './layout/user_text_input'
import { MainContentView } from './layout/main_content'
import { ChatRoomView } from './Chatroom'
import { WebsocketManager } from './utility/websocket_manager'
import { Get_WS } from './types/api_static'

export let wsContext = createContext<WebsocketManager | undefined>(undefined);

function App() {
  let [socket, setSocket] =  useState<WebsocketManager>();

  useEffect(() => {
    let websocket_manager = new WebsocketManager();
    websocket_manager.connect(Get_WS());

    setSocket(websocket_manager);
    return () => {
    };
  }, []);
  
  return (
    <wsContext.Provider value={socket}>
      <div className="h-screen">
        <ChatRoomView></ChatRoomView>
      </div>
    </wsContext.Provider>
  )
}

export default App
