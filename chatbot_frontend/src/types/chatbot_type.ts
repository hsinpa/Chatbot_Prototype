export interface MessageInterface {
    _id: string,
    content: string,
    type: 'user' | 'ai' | 'system',
    version: number
}