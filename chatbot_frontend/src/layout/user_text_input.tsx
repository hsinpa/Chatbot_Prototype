import { useEffect, useState } from "react"

export const User_Text_Input = function() {
    const [is_focus, set_focus] = useState(false);
    const [textarea_value, set_textarea] = useState('');

    let set_textarea_height = function() {
        let lineBreaks = textarea_value.match(/\n/g);
        let line_break_lens = (lineBreaks == undefined) ? 0 : lineBreaks.length;

        let textarea_dom = document.querySelector<HTMLTextAreaElement>('.user_input_textarea textarea');
        if (line_break_lens == undefined) line_break_lens = 0;
        
        let base = 3.5;
        let step = 1.8;
        if (textarea_dom != null)
            textarea_dom.style.height = ( (base) + (line_break_lens * step) )+ "em";
    }

    let fire_submit_event = function() {
        console.log(textarea_value);
        var lineBreaks = textarea_value.match(/\n/g);
        console.log('line break '+lineBreaks?.length)

        set_textarea('');
    }
    
    let on_textarea_change = function(e: React.FormEvent<HTMLTextAreaElement>) {
        set_textarea(e.currentTarget.value);
    }

    useEffect(() => {
        set_textarea_height();
    }, [textarea_value]);

    return (
        <div className="flex row-auto user_input_textarea">
            <textarea placeholder="Message with bot"
                onChange={on_textarea_change}
                onFocus={(x) => set_focus(true) }
                onBlur={(x) => {
                    set_focus(false) 
                    set_textarea_height()
                }}
                value={textarea_value}
                className="bg-slate-50 w-full resize-none rounded p-4 max-h-40 focus:outline-none">
            </textarea>
            <button className="bg-slate-300 px-2" onClick={fire_submit_event}>Send</button>
        </div>
    )
}