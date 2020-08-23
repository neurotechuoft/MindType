export interface Theme {
    key: {
        // The color of the text/symbol on a key
        text: string;
        // The background color of keys in each state
        background: { 
            neutral: string;
            flashed: string;
            selected: string;
        }
    },
    inputBar: {
        // The color of the text in the input bar
        text: string;
        // The background color of the input bar
        background: string;
        // The color of the border around the input bar
        border: string;
    },
    screen: {
        // The background color of a screen
        background: string;
    }
}

export const defaultTheme: Theme = {
    key: {
        text: "#ffffff",         //white
        background: {
            neutral: "#43a8c2",  //cyan
            flashed: "#facb33",  //sunglow yellow 
            selected: "#ab0020", //crimson red
        }
    },
    inputBar: {
        text: "#000000",        //black
        background: "#ffffff",  //white
        border: "#43a8c2",      //cyan
    },
    screen: {
        background: "#ffffff",  //white
    }
};

export default defaultTheme;
