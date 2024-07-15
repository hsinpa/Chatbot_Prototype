import { BotInputBubbleComp } from "../components/BotInputBubble";
import { UserInputBubbleComp } from "../components/UserInputBubble";

export const MainContentView = function() {
    return (
        <main className="bg-white flex-1 overflow-y-scroll">
            <div className="px-4 py-2">

                <UserInputBubbleComp></UserInputBubbleComp>
                <BotInputBubbleComp></BotInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
                <UserInputBubbleComp></UserInputBubbleComp>
            </div>
        </main>
    );
}