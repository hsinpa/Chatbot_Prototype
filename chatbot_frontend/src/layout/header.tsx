export const Header_Comp = function({chatbot_name}: {chatbot_name: string} ) {

    return (
        <div className="sticky top-0">
            <h2>{chatbot_name}</h2>
        </div>
    );
}