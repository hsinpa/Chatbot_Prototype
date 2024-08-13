import { memo, useContext, useEffect } from "react";
import { BotInputBubbleComp } from "../components/BotInputBubble";
import { UserInputBubbleComp } from "../components/UserInputBubble";
import { MessageInterface } from "../types/chatbot_type";
import { useMessageStore } from "../zusland/MessageStore";
import { wsContext } from "../App";
import { Clamp } from "../utility/utility_func";
import { NarratorBubbleComp } from "../components/NarratorBubble";


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
    let message_id_array = useMessageStore(state=>state.message_array)
    let get_message_func = useMessageStore(state=>state.get_message)
    let update_message_func = useMessageStore(state=>state.update_message)
    let push_message_func = useMessageStore(state=>state.push_message)

    let socket_manager = useContext(wsContext);

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
        console.log(socket_manager);

        socket_manager?.ListenToEvent('websocket', on_socket_message);

        return () => {
            socket_manager?.Deregister('websocket');
        }

    }, [socket_manager])
    

    useEffect(() => {
        cal_container_height(true);

    }, [message_id_array])

    return (
        <main className="message_container bg-white flex-1 overflow-y-scroll">
            <div className="px-4 py-2 flex flex-col gap-2">
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