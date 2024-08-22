import { memo, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useUIStore } from "../zusland/UIStore";
import { useShallow } from "zustand/react/shallow";
import side_panel_svg from '../assets/sprite/side_panel.svg';
import chest_svg from '../assets/sprite/chest.svg';
import check_list_svg from '../assets/sprite/check-list.svg';
import { SidebarTab } from "../utility/static_text";
import { API, CombineAPI, GetWebOptions } from "../types/api_static";
import { FormatString } from "../utility/utility_func";
import { SideBarItemBox } from "../components/SideBarItemBox";
import { MemoryInterface } from "../types/chatbot_type";
import { wsContext } from "../App";

export const MainSidebarView = function() {
    const ui_panel_flag = useUIStore(useShallow(s => s.side_panel_flag));
    const set_panel_flag = useUIStore(s => s.set_side_panel);
    const [tab, set_tab] = useState(SidebarTab.Inventory);
    const [memory, set_memory] = useState<MemoryInterface[]>([]);
    let socket_manager = useContext(wsContext);

    const fetch_memory = async function(user_id: string, session_id: string) {
        let url = CombineAPI(FormatString(API.Fetch_Memory, [user_id, session_id]));
        let memory_json: MemoryInterface[] = await (await fetch(url)).json();

        set_memory(memory_json);
    }

    const on_socket_message = function(event_id: string, json_data: any) {
        // try {
            if (json_data['event'] == 'memory') {
                console.log('Memory Update');
                let web_option = GetWebOptions();

                if (web_option != null)
                    fetch_memory(web_option.user_id, web_option.session_id)
            }
        // } catch {

        // }
    }


    const Render_Sidebar_Header = function() {
        return (
            <div className="flex flex-row">
                <img src={side_panel_svg} className="cursor-pointer	w-10 rounded-md p-1 hover:bg-slate-300"
                 onClick={() => set_panel_flag(!ui_panel_flag)}></img>

                {/* <img src={chest_svg} className={`cursor-pointer ml-auto	w-10 rounded-md p-1 hover:bg-slate-300
                ${ui_panel_flag ?'bg-sky-100':''}
                `}
                 onClick={() => {}}></img>

                <img src={check_list_svg} className={`cursor-pointer w-10 rounded-md p-1 hover:bg-slate-300`}
                 onClick={() => {}}></img> */}
            </div>
        );
    }

    const Render_Sidebar = function({children}: {children?: React.ReactNode | undefined}) {

        if (!ui_panel_flag) return <></>;

        return(
            <div className="flex flex-col h-full">
                { Render_Sidebar_Header() }

                {children}
            </div>
        )
    }


    useEffect(() => {
        socket_manager?.ListenToEvent('websocket', 'sidebar_socket', on_socket_message);

        return () => {
            socket_manager?.Deregister('websocket', 'sidebar_socket');
        }

    }, [socket_manager]);
    
    useEffect(() => {
        let web_option = GetWebOptions();
        if (web_option != null)
            fetch_memory(web_option.user_id, web_option.session_id);

    }, []);

    return (
        <div className={`side-panel bg-gray-100 h-full flex flex-col w-0 transition-all ${ui_panel_flag ? "p-1 w-72": ""}`}>
            <Render_Sidebar>
                <div className="flex flex-col grow overflow-y-scroll">
                    {
                        memory.map(x => <SideBarItemBox key={x.id} memory_data={x} ></SideBarItemBox>)
                    }
                </div>
            </Render_Sidebar>
        </div> 
   );
}