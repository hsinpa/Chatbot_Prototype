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