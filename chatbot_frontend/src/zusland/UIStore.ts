import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

type UIStoreState = {
    side_panel_flag: boolean,

    set_side_panel(enable: boolean): void,
}

export const useUIStore = create<UIStoreState>()(
    immer((set, get) => ({
        side_panel_flag: false,
        set_side_panel(enable: boolean) {
            set(state => {
                state.side_panel_flag = enable;
            })
        }
    })   
    )
)
