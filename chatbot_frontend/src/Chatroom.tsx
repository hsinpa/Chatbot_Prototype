import { useContext, useEffect } from "react"
import { Header_Comp } from "./layout/header"
import { MainContentView } from "./layout/main_content"
import { User_Text_Input } from "./layout/user_text_input"
import { wsContext } from "./App"
import { MainMessageView } from "./layout/main_message"
import { MainSidebarView } from "./layout/main_sidebar"
// https://tailwindflex.com/@manon-daniel/chat-template

export const ChatRoomView = function() {

    return (
      <div className="h-full flex flex-row">
        <MainSidebarView></MainSidebarView>

        <div className="h-full w-auto flex flex-col grow">
          <Header_Comp chatbot_name='Hsinpa bot'></Header_Comp>
          <MainContentView></MainContentView>    
          <div className="bg-gray-100 px-4 py-2">
            <User_Text_Input></User_Text_Input>
          </div>
        </div>
    </div>

    )
}