// Represents constants used by the Presenter

const CLASSES = {
    /* FOR POSITION */
    ROW: "row-", // used as: 'row-0', 'row-1', etc.
    COL: "col-", // used as: 'col-0', 'col-1', etc.
    /* FOR SIZE */
    // These are in the form of <attribute>-<num>, where <attribute> is directly proportional to <num>
    // Ex: width-<num> has exactly <n> times the width of width-1
    WIDTH: "width-", // must be used as 'width-1', 'width-2', etc.
    /* FOR SELECTION */
    IN_SCOPE: "in-scope", // possible to select in this round (ie: after selecting row-0, all buttons in this row are in scope)
    NOT_IN_SCOPE: "not-in-scope",
    HIGHLIGHTED: "highlighted", // currently an option to select (ie: currently flashed a different colour)
    NOT_HIGHLIGHTED: "not-highlighted"
};

const KEYS = {
    BUTTON: "button-", // used as: 'button-0', 'button-1', etc.
    BREAK: "break-" // used as: 'break-0', 'break-1', etc.
}

export {CLASSES, KEYS};
