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
    SELECTED: "selected",
    UNSELECTED: "unselected"
};

export {CLASSES};
