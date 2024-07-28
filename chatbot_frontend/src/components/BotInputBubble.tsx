export const BotInputBubbleComp = function({content}: {content: string}) {
    return (
        <div className="flex items-start p-2 bg-neutral-200 rounded-lg">
            <pre className="whitespace-pre-wrap overflow-x-auto break-words">{content}</pre>
        </div>
    );
}