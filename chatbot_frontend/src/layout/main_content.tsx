import { useContext, useEffect } from "react";
import { BotInputBubbleComp } from "../components/BotInputBubble";
import { UserInputBubbleComp } from "../components/UserInputBubble";
import { MessageInterface } from "../types/chatbot_type";
import { useMessageStore } from "../zusland/MessageStore";
import { wsContext } from "../App";

const RenderBubbleComp = function({comp}: {comp : MessageInterface | undefined}) {
    if (comp == undefined) return <></>

    if (comp.type == 'ai')   {
        return <BotInputBubbleComp content={comp.content}></BotInputBubbleComp>
    }

    if (comp.type == 'user') {
        return <UserInputBubbleComp content={comp.content}></UserInputBubbleComp>
    }
}


export const MainContentView = function() {
    let message_id_array = useMessageStore(state=>state.message_array)
    let get_message_func = useMessageStore(state=>state.get_message)
    let socket_manager = useContext(wsContext);

    const on_socket_message = function(json_data: any) {
        console.log(json_data);
    }

    useEffect(() => {
        socket_manager?.ListenToEvent('socket', on_socket_message);
        
        return () => {
            socket_manager?.Deregister('socket');
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