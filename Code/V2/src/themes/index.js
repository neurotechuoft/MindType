/* 
    script: color of the script on a key (number, letter, etc.)
    key: color of a key in a neutral state
    flashed: color of a key while flashed
    selected: color of a key currently selected by the user
*/

export const defaultTheme = {
    script: "#43a8c2",      //cyan      
    key: "#ffffff",         //white       
    flashed: "#ffff3c",     //yellow    
    selected: "#ee8426",    //orange
};

export const darkTheme = {
    script: "#b6b6b6",      //gray      
    key: "#000000",         //black       
    flashed: "#9f0c0c",     //dark red    
    selected: "#0807a0",    //dark blue
};

export const lightTheme = {
    script: "#000000",      //black      
    key: "#ffffff",         //white       
    flashed: "#9f0c0c",     //dark red    
    selected: "#0807a0",    //dark blue
}
