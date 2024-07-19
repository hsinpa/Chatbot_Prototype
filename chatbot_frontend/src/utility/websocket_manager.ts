import { v4 as uuidv4 } from 'uuid';
import EventSystem from './event_system';

export class WebsocketManager extends EventSystem {
    private _socket: WebSocket | null = null;
    private _id: string = '';

    get id() {
        return this._id;
    }

    get is_connect() {
        return this._socket != null && this._socket.readyState == WebSocket.OPEN
    }

    send(json_string: string) {
        if (this._socket?.readyState == WebSocket.OPEN)
            this._socket?.send(json_string);
    }

    connect(url: string) {
        this._socket = new WebSocket(url);

        // this._socket.addEventListener("open", (event) => {
        //     console.log('socket on connect');
        //     this._socket?.send("Hello Server!");
        // });
        
        this._socket.addEventListener("message", (event) => {

            try {
                let json = JSON.parse(event.data);

                if (!('event' in json)) return;

                if ('_id' in json) 
                    this._id = json['_id']

                // console.log("Message from server ", event.data);

                this.Notify('websocket', json);
            } catch {

            }
        });
    }
}

