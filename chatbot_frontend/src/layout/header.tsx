import { useUIStore } from "../zusland/UIStore";
import side_panel_svg from '../assets/sprite/side_panel.svg';

export const Header_Comp = function({chatbot_name}: {chatbot_name: string} ) {

    const ui_store = useUIStore()


    const expand_side_panel = function() {

    }

    return (
        <div className="sticky top-0 flex flex-row items-center gap-4">
            <img src={side_panel_svg} className="cursor-pointer	w-10 rounded-md p-1 hover:bg-slate-300"></img>
            <h2>{chatbot_name}</h2>
        </div>
    );
}