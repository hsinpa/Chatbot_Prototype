import { useContext, useEffect } from "react"
import { Header_Comp } from "./layout/header"
import { MainContentView } from "./layout/main_content"
import { User_Text_Input } from "./layout/user_text_input"
import { wsContext } from "./App"
// https://tailwindflex.com/@manon-daniel/chat-template

export const ChatRoomView = function() {
    // let socket = useContext(wsContext)

    // useEffect(() => {
    //   socket?.send(JSON.stringify({'hello': 'world'}))
    // }, [socket])

    return (
        <div className="h-full flex flex-col">

        <Header_Comp chatbot_name='Hsinpa bot'></Header_Comp>
        <MainContentView></MainContentView>    
        <div className="bg-gray-100 px-4 py-2">
          <User_Text_Input></User_Text_Input>
        </div>
        
    </div>
    )
}