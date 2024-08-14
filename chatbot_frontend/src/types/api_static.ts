import { WebParamInterface } from "./chatbot_type";

export let ENV = 'dev';

let SELF_DOMAIN = 'localhost:8842';
let SELF_HTTP = 'http://';
let SELF_SOCKET = 'ws://';

let PROD_DOMAIN = 'localhost:8842';
let PROD_HTTP = 'https://';
let PROD_SOCKET = 'wss://';

export const DOMAIN = (ENV == 'dev') ? SELF_DOMAIN : PROD_DOMAIN;
export const HTTP = (ENV == 'dev') ? SELF_HTTP : PROD_HTTP;
export const SOCKET = (ENV == 'dev') ? SELF_SOCKET : PROD_SOCKET;

export const Get_WS = function() {
    return SOCKET+SELF_DOMAIN+'/ws';
}

export const Get_HTTP = function() {
    return HTTP+DOMAIN;
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