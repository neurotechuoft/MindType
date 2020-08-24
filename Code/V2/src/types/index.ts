/**
 * The type (or category of functionality) that a key falls into.
 */
export enum KeyType {
    // A key that is use to type text
    TEXT = 'text',
    // A key that is used to switch screens / keyboards
    NAVIGATION = 'navigation',
}

/**
 * The state that a key is in.
 */
export enum KeyStatus {
    // The default state
    NEUTRAL = 'neutral',
    // The flashed/highlighted key (that is not selected)
    FLASHED = 'flashed',
    // The selected key
    SELECTED = 'selected',
}
