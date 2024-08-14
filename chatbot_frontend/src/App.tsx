import { createContext, useEffect, useState } from 'react'
import { Header_Comp } from './layout/header'
import { User_Text_Input } from './layout/user_text_input'
import { MainContentView } from './layout/main_content'
import { ChatRoomView } from './Chatroom'
import { WebsocketManager } from './utility/websocket_manager'
import { Get_WS, GetWebOptions } from './types/api_static'
import { v4 as uuidv4 } from 'uuid';

export let wsContext = createContext<WebsocketManager | undefined>(undefined);

function App() {
  let [socket, setSocket] =  useState<WebsocketManager>();

  useEffect(() => {
    let web_option = GetWebOptions();

    // If user id or session id not exist, assign them one
    if (web_option == null) {
      var url = new URL(window.location.href);
      url.searchParams.set('user_id', uuidv4());
      url.searchParams.set('session_id', uuidv4());

      window.location.href = url.toString();
      return;
    }

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
