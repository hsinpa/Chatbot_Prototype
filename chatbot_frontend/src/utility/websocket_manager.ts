import { v4 as uuidv4 } from 'uuid';
import EventSystem from './event_system';

export class WebsocketManager extends EventSystem {
    private _socket: WebSocket | null = null;
    private _id: string = '';

    get id() {
        return this._id;
    }

    connect(url: string) {
        this._socket = new WebSocket(url);

        // this._socket.addEventListener("open", (event) => {
        //     console.log('socket on connect');
        //     this._socket?.send("Hello Server!");
        // });
        
        this._socket.addEventListener("message", (event) => {
            console.log("Message from server ", event.data);

            try {
                let json = JSON.parse(event.data);
                if ('_id' in json) 
                    this._id = json['id']

                this.Notify('websocket', json);
            } catch {

            }
        });
    }
}

