export const UserInputBubbleComp = function({content}: {content: string}) {
    return (
        <div className="flex items-center justify-end p-1">
            <pre className="max-w-lg whitespace-pre-wrap overflow-x-auto break-words bg-neutral-200 p-2 rounded-md">{content}</pre>
        </div>
    );
}