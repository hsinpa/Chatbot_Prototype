import { useState } from 'react'
import { Header_Comp } from './layout/header'
import { User_Text_Input } from './layout/user_text_input'
import { MainContentView } from './layout/main_content'
import { ChatRoomView } from './Chatroom'

function App() {
  return (
<div className="h-screen">
  <ChatRoomView></ChatRoomView>
</div>

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
