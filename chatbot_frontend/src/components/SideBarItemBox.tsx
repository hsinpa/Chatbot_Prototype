import { MemoryInterface } from "../types/chatbot_type";

export const SideBarItemBox =  function({memory_data}: {memory_data: MemoryInterface}) {
    
    
    
    
    return (
        <div className="flex flex-col p-2">
            <div className="text-center rounded-tr rounded-tl bg-sky-400 font-semibold">
                {memory_data.attribute.toUpperCase()}
            </div>

            <p className="p-4 bg-sky-50">
                {memory_data.body}
            </p>
        </div>
    );
}