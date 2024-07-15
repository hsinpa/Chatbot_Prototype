export const UserInputBubbleComp = function() {
    return (
        <div className="flex items-center justify-end p-2 rounded-lg">
            <pre className="max-w-lg whitespace-pre-wrap overflow-x-auto break-words bg-neutral-200">So if you want to position child element to right of parent element you can use margin-left
                : auto but now child 
                element will also push other
                div to the right as you can see here Fiddle.
            </pre>
        </div>
    );
}