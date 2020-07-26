/**
 * The application's color scheme.
 *
 * view.background: background color of the views
 *
 * key.text: the color of the script on a key (number, letter, etc.)
 * key.background: the key's background color in each state
 *
 * inputBar.text: color of text in the textbar
 * inputBar.background: color of background of textbar
 * inputBar.border: color of border of textbar
 */
interface Theme {
    view: {
        background: String,
    }
    key: {
        text: String,
        background: {
            neutral: String,
            flashed: String,
            selected: String,
        },
    },
    inputBar: {
        text: String,
        background: String,
        border: String,
    },
}

const defaultTheme: Theme = {
    view: {
        background: '#ffffff', //white
    },
    key: {
        text: '#43a8c2', //cyan
        background: {
            neutral: '#ffffff', //white
            flashed: '#ffff3c', //yellow
            selected: '#ee8426', //orange
        },
    },
    inputBar: {
        text: '#000000', //black
        background: '#ffffff', //white
        border: '#43a8c2', //cyan
    },
};

export default defaultTheme;
