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

    // <div className='flex content-center justify-center '>
    //   <div className='w-9/12 flex flex-col min-h-screen justify-between overflow-hidden'>
    //     <Header_Comp chatbot_name='Hsinpa bot'></Header_Comp>

    //     <div className='flex-1 relative flex-wrap max-h-fit'>
    //         <MainContentView></MainContentView>
    //     </div>
        
    //     <User_Text_Input></User_Text_Input>
    //   </div>
    // </div>

  )
}

export default App
