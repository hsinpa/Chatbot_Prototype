import { MainMessageView } from "./main_message";
import { MainSidebarView } from "./main_sidebar";

export const MainContentView = function() {

    return (
        <div className="bg-white flex-1 flex overflow-y-scroll flex-row">
            <MainSidebarView></MainSidebarView>
            <MainMessageView></MainMessageView>    
        </div>
    );
}