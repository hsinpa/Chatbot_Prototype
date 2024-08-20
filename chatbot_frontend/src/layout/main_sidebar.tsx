import { memo, useCallback, useEffect, useMemo, useState } from "react";
import { useUIStore } from "../zusland/UIStore";
import { useShallow } from "zustand/react/shallow";
import side_panel_svg from '../assets/sprite/side_panel.svg';
import chest_svg from '../assets/sprite/chest.svg';
import check_list_svg from '../assets/sprite/check-list.svg';
import { SidebarTab } from "../utility/static_text";
import { API, CombineAPI, GetWebOptions } from "../types/api_static";
import { FormatString } from "../utility/utility_func";

export const MainSidebarView = function() {
    const ui_panel_flag = useUIStore(useShallow(s => s.side_panel_flag));
    const set_panel_flag = useUIStore(s => s.set_side_panel);
    const [tab, set_tab] = useState(SidebarTab.Inventory);


    const fetch_memory = async function(user_id: string, session_id: string) {
        let url = CombineAPI(FormatString(API.Fetch_Memory, [user_id, session_id]));
        let messages: any[] = await (await fetch(url)).json();


        console.log(messages)

    }

    const Render_Sidebar_Header = function() {
        return (
            <div className="flex flex-row">
                <img src={side_panel_svg} className="cursor-pointer	w-10 rounded-md p-1 hover:bg-slate-300"
                 onClick={() => set_panel_flag(!ui_panel_flag)}></img>

                <img src={chest_svg} className={`cursor-pointer ml-auto	w-10 rounded-md p-1 hover:bg-slate-300
                ${ui_panel_flag ?'bg-sky-100':''}
                `}
                 onClick={() => {}}></img>

                <img src={check_list_svg} className={`cursor-pointer w-10 rounded-md p-1 hover:bg-slate-300`}
                 onClick={() => {}}></img>
            </div>
        );
    }

    const Render_Sidebar = function({children}: {children?: React.ReactNode | undefined}) {

        if (!ui_panel_flag) return <></>;

        return(
            <div>
                { Render_Sidebar_Header() }
            </div>
        )
    }

    useEffect(() => {
        let web_option = GetWebOptions();
        if (web_option != null)
            fetch_memory(web_option.user_id, web_option.session_id);

    }, []);

    return (
        <div className={`side-panel bg-gray-100 h-full flex flex-col w-0 transition-all ${ui_panel_flag ? "p-1 w-60": ""}`}>
            <Render_Sidebar></Render_Sidebar>
        </div> 
   );
}