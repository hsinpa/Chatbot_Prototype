import { WebParamInterface } from "./chatbot_type";

export const API = Object.freeze({
    'Fetch_History': '/chatbot/message_history/user/{0}/session/{1}',
    'Fetch_Memory': '/chatbot/memory/user/{0}/session/{1}'
});

export const Get_WS = function() {
    return import.meta.env.VITE_WSS_DOMAIN;
}

export const Get_HTTP = function() {
    return import.meta.env.VITE_API_DOMAIN;
}

export const CombineAPI = function(url: string) {
    return Get_HTTP() + url;
}

export const GetWebOptions = function() {
    let params = new URLSearchParams(window.location.search);
    let user_id = params.get("user_id");
    let session_id = params.get("session_id");

    if (user_id == undefined || session_id == undefined) return null;

    let options: WebParamInterface = {
        user_id : user_id,
        session_id : session_id,
    };

    return options;
} 