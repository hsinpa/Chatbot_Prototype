class EventSystem {
    
    _events : any;

    constructor() {
        this._events = {};
    }
    
    ListenToEvent(event_id : string, callback : any) {

        if (this._events.hasOwnProperty(event_id)) {
            this._events[event_id] = callback;
            return;
        }

        this._events[event_id] = [callback];
    }

    Deregister(event_id : string) {
        if (this._events.hasOwnProperty(event_id)) {
            delete this._events[event_id]
        }
    }

    Notify(event_id : string, parameters? : any) {
        if (this._events.hasOwnProperty(event_id) && this._events[event_id] != null) {
            this._events[event_id](event_id, parameters)
        }  
    }
}

export default EventSystem;