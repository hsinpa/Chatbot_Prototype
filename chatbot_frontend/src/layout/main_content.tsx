import { memo, useContext, useEffect } from "react";
import { BotInputBubbleComp } from "../components/BotInputBubble";
import { UserInputBubbleComp } from "../components/UserInputBubble";
import { MessageInterface } from "../types/chatbot_type";
import { useMessageStore } from "../zusland/MessageStore";
import { wsContext } from "../App";

const RenderBubbleComp = memo(function({comp}: {comp : MessageInterface | undefined}) {
    if (comp == undefined) return <></>

    if (comp.type == 'ai')   {
        return <BotInputBubbleComp content={comp.content}></BotInputBubbleComp>
    }

    if (comp.type == 'user') {
        return <UserInputBubbleComp content={comp.content}></UserInputBubbleComp>
    }
}, arePropsEqual);

function arePropsEqual(oldProps: {comp: MessageInterface | undefined}, 
                        newProps: {comp: MessageInterface | undefined}) {

    if (oldProps.comp == undefined || newProps.comp == undefined) return true;
    return !(newProps.comp.version > oldProps.comp.version);                     
}

export const MainContentView = function() {
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
                        type: 'ai',
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
    
    return (
        <main className="bg-white flex-1 overflow-y-scroll">
            <div className="px-4 py-2">
                {
                    message_id_array.map(x => {
                        return <RenderBubbleComp key={x} comp={get_message_func(x)}></RenderBubbleComp>;
                    })
                }

                {/* <UserInputBubbleComp></UserInputBubbleComp>
                <BotInputBubbleComp></BotInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp> */}
            </div>
        </main>
    );
}