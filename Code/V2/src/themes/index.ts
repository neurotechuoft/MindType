import { KeyType, KeyStatus } from '../types';

/**
 * The colors of a key for a single 'KeyStatus'.
 */
export interface KeyStatusColor {
    // The color of the text/symbol on a key
    content: string;
    // The background color of the key
    background: string;
}

/**
 * The colors of a key for a single 'KeyType',
 * but for every 'KeyStatus'.
 */
export interface KeyTheme {
    // The font family for text on a key
    font: string;
    color: {
        // The colors used on a key for each status
        [key in KeyStatus]: KeyStatusColor
    }
}

/**
 * The theme of the entire application.
 */
interface Theme {
    key: {
        [key in KeyType]: KeyTheme
    }
    inputBar: {
        // The font family for text in the input bar
        font: string;
        color: {
            // The color of the text in the input bar
            text: string;
            // The background color of the input bar
            background: string;
            // The color of the border around the input bar
            border: string;
        }
    },
    screen: {
        // The font family for the text directly on the screen
        font: string;
        color: {
            // The background color of a screen
            background: string;
        }
    }
}

const WHITE = '#FFFFFF';
const LIGHT_CYAN = '#D5FAFF';
const LIGHT_BLUE = '#52A0B4';
const DARK_BLUE = '#00627B';
const PRIMARY_FONT = 'Helvetica Neue';

const defaultTheme: Theme = {
    key: {
        text: {
            font: PRIMARY_FONT,
            color: {
                neutral: {
                    content: LIGHT_BLUE,
                    background: WHITE,
                },
                flashed: {
                    content: WHITE,
                    background: LIGHT_BLUE,
                },
                selected: {
                    content: WHITE,
                    background: DARK_BLUE,
                }
            }
        },
        navigation: {
            font: PRIMARY_FONT,
            color: {
                neutral: {
                    content: LIGHT_BLUE,
                    background: LIGHT_CYAN,
                },
                flashed: {
                    content: WHITE,
                    background: LIGHT_BLUE,
                },
                selected: {
                    content: WHITE,
                    background: DARK_BLUE,
                }
            }
        },
    },
    inputBar: {
        font: PRIMARY_FONT,
        color: {
            text: LIGHT_BLUE,
            background: LIGHT_CYAN,
            border: LIGHT_CYAN,
        }   
    },
    screen: {
        font: PRIMARY_FONT,
        color: {
            background: LIGHT_BLUE,
        }
    }
};

export default defaultTheme;
