import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {isRequired, isPositiveInteger, isNonNegativeInteger} from "./PropTypes";
import {CLASSES} from "./Constants";

/**
 * Creates a Button of Dynamic Width.
 *
 * props.content: The contents of the button.
 * props.row: The row of the button within its grid.
 * props.col: the col of the button within its grid.
 * props.width: The width of the button. Optional.
 */
class Button extends Component {

    static propTypes = {
        content: PropTypes.any.isRequired,
        row(props, propName, component) {
            isRequired(props, propName);
            isNonNegativeInteger(props, propName);
        },
        col(props, propName, component) {
            isRequired(props, propName);
            isNonNegativeInteger(props, propName);
        },
        width: PropTypes.number // Note: more validation in constructor
    };

    constructor(props) {
        super(props);
        this.state = {
            width: this.props.width ? this.props.width : 1
        };
        isPositiveInteger(this.state, 'width'); // Type Validation
        this.setWidth = this.setWidth.bind(this);
        this.incrementWidth = this.incrementWidth.bind(this);
    }

    componentDidMount() {
        this.props.onRef(this);
    }

    componentWillUnmount() {
        this.props.onRef(undefined);
    }

    setWidth(newWidth) {
        this.state.width = newWidth;
    }

    /**
     * Increase the width of the button.
     *
     * @param amount - value to increment integer representing width.
     *           If not specified, defaults to 1.
     */
    incrementWidth(amount) {
        if (amount === null) {
            amount = 1;
        }
        this.state.width += amount;
    }

    render() {
        let {content, row, col} = this.props;
        let {width} = this.state;

        let defaultClasses = CLASSES.UNSELECTED;
        let allClasses = defaultClasses + " "
            + CLASSES.ROW + row + " "
            + CLASSES.COL + col + " "
            + CLASSES.WIDTH + width;

        return (
            <button className={allClasses}>
                {content}
            </button>
        );
    }
}

export default Button;
