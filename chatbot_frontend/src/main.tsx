import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { Get_WS } from './types/api_static.ts';

// const socket = new WebSocket(Get_WS());

// // Connection opened
// socket.addEventListener("open", (event) => {
//   socket.send("Hello Server!");
// });

// // Listen for messages
// socket.addEventListener("message", (event) => {
//   console.log("Message from server ", event.data);
// });

  // <React.StrictMode>
  // <App />
  /* </React.StrictMode>, */


ReactDOM.createRoot(document.getElementById('root')!).render(
    <App />
)
