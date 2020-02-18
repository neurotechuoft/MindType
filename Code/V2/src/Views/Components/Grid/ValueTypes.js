// Custom Value Type Validation.
// Throws an error if requirement is unsatisfied.

function isRequired(name, value) {
    if (value == null) {
        throw new Error(name + ' should not be null');
    }
}

function isPositiveInteger(name, value) {
    let error = new Error(name + ' should be a positive integer (actual value: ' + value + ')');
    if (!Number.isInteger(value)) {
        throw error;
    }
    if (value < 1) {
        throw error;
    }
}

function isNonNegativeInteger(name, value) {
    let error = new Error(name + ' should be a non-negative integer (actual value: ' + value + ')');
    if (!Number.isInteger(value)) {
        throw error;
    }
    if (value < 0) {
        throw error;
    }
}

function isFunction(name, value) {
    if (!(value instanceof Function)) {
        throw new Error(name + ' is not a function');
    }
}

function isArray(name, value) {
    if (!Array.isArray(value)) {
        throw new Error(name + ' is not an array');
    }
}

function isArrayOfValidLength(name, value, expectedLength) {
    this.isArray(name, value);
    let actualLength = value.length;
    if(actualLength !== expectedLength) {
        throw new Error(name + ' has array length ' + actualLength + ' (expected length ' + expectedLength +')');
    }
}

export {isRequired, isPositiveInteger, isNonNegativeInteger, isFunction, isArray, isArrayOfValidLength};
