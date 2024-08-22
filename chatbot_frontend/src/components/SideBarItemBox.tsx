import { MemoryInterface } from "../types/chatbot_type";

    
const STYLE_TABLE = {
    'Knowledge': {
        'header_color': 'bg-sky-400',
        'body_color': 'bg-sky-50',
    },

    'Item': {
        'header_color': 'bg-red-400',
        'body_color': 'bg-red-50',
    },
};


export const SideBarItemBox =  function({memory_data}: {memory_data: MemoryInterface}) {

    let style = STYLE_TABLE[memory_data.attribute];

    return (
        <div className="flex flex-col p-2">
            <div className={`text-center rounded-tr rounded-tl font-semibold ${style.header_color}`}>
                {memory_data.attribute.toUpperCase()}
            </div>

            <p className={`p-4 ${style.body_color}`}>
                {memory_data.body}
            </p>
        </div>
    );
}