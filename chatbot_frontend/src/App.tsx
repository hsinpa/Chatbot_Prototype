import { useState } from 'react'
import { Header_Comp } from './layout/header'
import { User_Text_Input } from './layout/user_text_input'

function App() {
  return (

    <div className='flex content-center justify-center'>
      <div className='w-9/12 flex flex-col min-h-screen justify-between'>
        <Header_Comp chatbot_name='Hsinpa bot'></Header_Comp>
        <main className="mb-auto h-10 bg-green-500">Content</main>
        <User_Text_Input></User_Text_Input>

      </div>
    </div>

  )
}

export default App
