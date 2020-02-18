// Custom PropType Validation

function isRequired(props, propName) {
    if (!(propName in props)) {
        throw new Error('missing prop ' + propName);
    }
}

function isPositiveInteger(props, propName) {
    let value = props[propName];
    let error = new Error('prop ' + propName + ' is not a positive integer (actual value: ' + value + ')');
    if (!Number.isInteger(value)) {
        throw error;
    }
    if (value < 1) {
        throw error;
    }
}

function isNonNegativeInteger(props, propName) {
    let value = props[propName];
    let error = new Error('prop ' + propName + ' should be a non-negative integer (actual value: ' + value + ')');
    if (!Number.isInteger(value)) {
        throw error;
    }
    if (value < 0) {
        throw error;
    }
}

function isArray(props, propName) {
    if (!Array.isArray(props[propName])) {
        throw new Error('prop ' + propName + ' is not an array');
    }
}

function isArrayOfValidLength(props, propName, expectedLength) {
    isArray(props, propName);
    let actualLength = props[propName].length;
    if(actualLength !== expectedLength) {
        throw new Error('prop ' + propName + ' has length ' + actualLength + ' (expected length ' + expectedLength +')');
    }
}

export {isRequired, isPositiveInteger, isNonNegativeInteger, isArray, isArrayOfValidLength};