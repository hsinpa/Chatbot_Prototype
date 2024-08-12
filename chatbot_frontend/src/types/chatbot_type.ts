 

export interface MessageInterface {
    _id: string,
    content: string,
    type: 'bot' | 'human' | 'narrator',
    version: number
}