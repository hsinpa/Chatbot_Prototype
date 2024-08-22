class EventSystem {
    
    _events : any;

    constructor() {
        this._events = {};
    }
    
    ListenToEvent(event_id : string, key: string, callback : any) {

        if (this._events.hasOwnProperty(event_id)) {
            this._events[event_id][key] = callback;
            return;
        }

        this._events[event_id] = { key: callback};
    }

    Deregister(event_id : string, key: string) {
        if (this._events.hasOwnProperty(event_id)) {
            if (this._events[event_id].hasOwnProperty(key)) {
                delete this._events[event_id][key];
            }
        }
    }

    Notify(event_id : string, parameters? : any) {
        if (this._events.hasOwnProperty(event_id) && this._events[event_id] != null) {

            for (let key in this._events[event_id]) {
                this._events[event_id][key]?.(event_id, parameters);
            }

            // this._events[event_id](event_id, parameters)
        }  
    }
}

export default EventSystem;