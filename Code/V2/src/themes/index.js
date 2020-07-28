/* 
    key.script: the color of the script on a key (constant for all states)
    key.neutral: background color of a key in a neutral state
    key.flashed: background color of a key while flashed
    key.selected: background color of a key currently selected by the user

    inputBar.border: color of border of textbar
    inputBar.background: color of background of textbar
    inputBar.text: color of text in the textbar

    background: color of the background of the main view
*/

const defaultTheme = {

    key: {
        script: "#ffffff", //white
        neutral: "#43a8c2", //cyan
        flashed: "#facb33",  //sunglow yellow 
        selected: "#ab0020",    //crimson red
    },

    inputBar: {
        border: "#43a8c2",      //cyan
        background: "#ffffff",  //white
        text: "#000000",        //black
    },
    
    background: "#ffffff",      //white
    
};

export default defaultTheme;