import { memo, useContext, useEffect } from "react";
import { BotInputBubbleComp } from "../components/BotInputBubble";
import { UserInputBubbleComp } from "../components/UserInputBubble";
import { MessageInterface } from "../types/chatbot_type";
import { useMessageStore } from "../zusland/MessageStore";
import { wsContext } from "../App";
import { Clamp, FormatString } from "../utility/utility_func";
import { NarratorBubbleComp } from "../components/NarratorBubble";
import { API, CombineAPI, GetWebOptions } from "../types/api_static";


export const cal_container_height = function(force: boolean = false) {
    let container_dom = document.querySelector<HTMLDivElement>('.message_container');
    let container_parent = container_dom?.parentElement;

    if (container_dom == null || container_parent == null) return;

    let container_height = container_parent.offsetHeight;
    let scroll_value = container_parent.scrollHeight - container_parent.offsetHeight;
    let scroll_bottom = Clamp(scroll_value, 0, scroll_value);
    let scroll_error_offset = container_parent.scrollHeight - scroll_bottom;    
    let error_range = 5;

    if (scroll_error_offset <= error_range || force) {
        container_parent.scrollTo({top: scroll_bottom + container_parent.offsetHeight, behavior: "smooth"})
    }
}

const RenderBubbleComp = memo(function({comp}: {comp : MessageInterface | undefined}) {
    if (comp == undefined) return <></>

    if (comp.type == 'bot')   {
        return <BotInputBubbleComp content={comp.content}></BotInputBubbleComp>
    }

    if (comp.type == 'narrator')   {
        return <NarratorBubbleComp content={comp.content}></NarratorBubbleComp>
    }

    if (comp.type == 'human') {
        return <UserInputBubbleComp content={comp.content}></UserInputBubbleComp>
    }
}, arePropsEqual);

function arePropsEqual(oldProps: {comp: MessageInterface | undefined}, 
                        newProps: {comp: MessageInterface | undefined}) {

    if (oldProps.comp == undefined || newProps.comp == undefined) return true;
    return !(newProps.comp.version > oldProps.comp.version);                     
}

export const MainMessageView = function() {
    let message_id_array = useMessageStore(state => state.message_array)
    let get_message_func = useMessageStore(state => state.get_message)
    let update_message_func = useMessageStore(state => state.update_message)
    let push_message_func = useMessageStore(state => state.push_message)
    let clear_message_func = useMessageStore(state => state.clear)

    let socket_manager = useContext(wsContext);

    const fetch_sync_message = async function(user_id: string, session_id: string) {
        let url = CombineAPI(FormatString(API.Fetch_History, [user_id, session_id]));

        let messages: any[] = await (await fetch(url)).json();

        console.log(messages);
        for (let i = 0; i < messages.length; i++) {        
            let message_type = {
                _id: messages[i].bubble_id,
                content: messages[i].body,
                type: messages[i].message_type,
                version: 1
            }

            push_message_func(message_type);
        }
    }

    const on_socket_message = function(event_id: string, json_data: any) {
        // try {
            if (json_data['event'] == 'bot') {
                let bubble_id = json_data['bubble_id'];
                let index = json_data['index'];
                let data_chunk = json_data['data'];
                let current_message_struct = get_message_func(bubble_id);
                
                // Push
                if (current_message_struct == null) {
                    push_message_func({
                        _id: bubble_id, 
                        content: data_chunk,
                        type: json_data['identity'],
                        version: index
                    })
                } else {
                    current_message_struct.content += data_chunk;
                    current_message_struct.version = index;

                    update_message_func(current_message_struct);
                }
            }
        // } catch {

        // }
    }

    useEffect(() => {
        socket_manager?.ListenToEvent('websocket', 'main_content_socket', on_socket_message);

        return () => {
            socket_manager?.Deregister('websocket', 'main_content_socket');
        }

    }, [socket_manager])
    

    useEffect(() => {
        let web_option = GetWebOptions();
        if (web_option != null)
            fetch_sync_message(web_option.user_id, web_option.session_id);

        return () => {
            console.log('clear');
            clear_message_func();
        }


        }, []); 

    useEffect(() => {
        cal_container_height(true);

    }, [message_id_array])

    return (
        <main className="bg-white flex-1 overflow-y-scroll">
            <div className="message_container px-4 py-2 flex flex-col gap-2">
                {
                    message_id_array.map(x => {
                        return <RenderBubbleComp key={x} comp={get_message_func(x)}></RenderBubbleComp>;
                    })
                }

                {/* <UserInputBubbleComp content="Let’s take a detour to the land of citrus! Oh, the zesty burst of an orange or the refreshing tang of a lemon! These fruits are not only thirst-quenching but also a fantastic source of vitamin C. Imagine sipping on a cool glass of freshly squeezed lemonade on a hot summer day—pure bliss!"></UserInputBubbleComp>
                <BotInputBubbleComp content="Let’s take a detour to the land of citrus! Oh, the zesty burst of an orange or the refreshing tang of a lemon! These fruits are not only thirst-quenching but also a fantastic source of vitamin C. Imagine sipping on a cool glass of freshly squeezed lemonade on a hot summer day—pure bliss!"></BotInputBubbleComp>
                <UserInputBubbleComp content="Let’s take a detour to the land of citrus! Oh, the zesty burst of an orange or the refreshing tang of a lemon! These fruits are not only thirst-quenching but also a fantastic source of vitamin C. Imagine sipping on a cool glass of freshly squeezed lemonade on a hot summer day—pure bliss!"></UserInputBubbleComp>
                <BotInputBubbleComp content="Let’s take a detour to the land of citrus! Oh, the zesty burst of an orange or the refreshing tang of a lemon! These fruits are not only thirst-quenching but also a fantastic source of vitamin C. Imagine sipping on a cool glass of freshly squeezed lemonade on a hot summer day—pure bliss!"></BotInputBubbleComp>
                <UserInputBubbleComp content="Let’s take a detour to the land of citrus! Oh, the zesty burst of an orange or the refreshing tang of a lemon! These fruits are not only thirst-quenching but also a fantastic source of vitamin C. Imagine sipping on a cool glass of freshly squeezed lemonade on a hot summer day—pure bliss!"></UserInputBubbleComp>
                <BotInputBubbleComp content="Let’s take a detour to the land of citrus! Oh, the zesty burst of an orange or the refreshing tang of a lemon! These fruits are not only thirst-quenching but also a fantastic source of vitamin C. Imagine sipping on a cool glass of freshly squeezed lemonade on a hot summer day—pure bliss!"></BotInputBubbleComp> */}

            </div>
        </main>
    );
}