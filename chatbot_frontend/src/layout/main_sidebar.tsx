import { memo, useCallback, useEffect, useMemo, useState } from "react";
import { useUIStore } from "../zusland/UIStore";
import { useShallow } from "zustand/react/shallow";
import side_panel_svg from '../assets/sprite/side_panel.svg';
import chest_svg from '../assets/sprite/chest.svg';
import check_list_svg from '../assets/sprite/check-list.svg';
import { SidebarTab } from "../utility/static_text";

export const MainSidebarView = function() {
    const ui_panel_flag = useUIStore(useShallow(s => s.side_panel_flag));
    const set_panel_flag = useUIStore(s => s.set_side_panel);
    const [tab, set_tab] = useState(SidebarTab.Inventory);

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

    return (
        <div className={`side-panel bg-gray-100 h-full flex flex-col w-0 transition-all ${ui_panel_flag ? "p-1 w-60": ""}`}>
            <Render_Sidebar></Render_Sidebar>
        </div> 
   );
}