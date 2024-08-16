import { create } from "zustand"
import { MessageInterface } from "../types/chatbot_type"
import { immer } from "zustand/middleware/immer"
import {enableMapSet} from "immer"

enableMapSet();

type MessageStoreState = {
    message_array: string[],
    message_map: Map<string,MessageInterface>,

    get_message(id: string): MessageInterface | undefined,
    push_message(message: MessageInterface): void,
    update_message(message: MessageInterface): void
    clear(): void
}

export const useMessageStore = create<MessageStoreState>()(
    immer((set, get) => ({
        message_array: [],
        message_map: new Map(),

        get_message(id: string) {
            let msg = get().message_map.get(id);

            if (msg != undefined)
                return {...msg};

            return undefined;
        },

        push_message(message: MessageInterface) {
            set(state => {
                if (message._id in state.message_map) {
                    state.update_message(message);
                    return;
                }


                state.message_array.push(message._id);
                state.message_map.set(message._id, message);
            });
        },

        update_message(message: MessageInterface) {
            set(state => {
                state.message_array = [...state.message_array]
                state.message_map.set(message._id, {...message});
            });
        },

        clear() {
            set(state => {
                state.message_array =[];
                state.message_map.clear();
            });
        }
    })),
)
  