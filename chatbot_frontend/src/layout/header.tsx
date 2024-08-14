import { useUIStore } from "../zusland/UIStore";
import side_panel_svg from '../assets/sprite/side_panel.svg';

export const Header_Comp = function({chatbot_name}: {chatbot_name: string} ) {

    const ui_store = useUIStore()

    const expand_side_panel = function() {
        ui_store.set_side_panel(!ui_store.side_panel_flag);
    }

    const render_side_panel_btn = function() {
        if (ui_store.side_panel_flag) {
            return <></>
        } else {
            return <img src={side_panel_svg} className="cursor-pointer	w-10 rounded-md p-1 hover:bg-slate-300"
            onClick={expand_side_panel}></img>;
        }
    }

    return (
        <div className="sticky top-0 flex flex-row items-center gap-4 px-1 py-1">
            {render_side_panel_btn()}
            <h2>{chatbot_name}</h2>
        </div>
    );
}