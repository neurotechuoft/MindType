import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {isRequired, isPositiveInteger, isNonNegativeInteger} from "../PropTypes";
import {CLASSES, KEYS} from "../Constants";

/**
 * Creates a Button of Dynamic Width, which can also be:
 * - in scope / not in scope
 * - highlighted / not hightlighted
 *
 * props.content: The contents of the button.
 * props.row: The row of the button within its grid.
 * props.col: the col of the button within its grid.
 * props.width: The width of the button.
 *
 */
class Button extends Component {

    static propTypes = {
        content: PropTypes.any.isRequired,
        onClick: PropTypes.func,
        row(props, propName, component) {
            isRequired(props, propName);
            isNonNegativeInteger(props, propName);
        },
        col(props, propName, component) {
            isRequired(props, propName);
            isNonNegativeInteger(props, propName);
        },
        width(props, propName, component) {
            isRequired(props, propName);
            isPositiveInteger(props, propName);
        }
    };

    constructor(props) {
        super(props);
        this.state = {
            width: this.props.width,
            inScope: true,
            highlighted: false
        };
        this.onClick = this.props.onClick;
        this.setWidth = this.setWidth.bind(this);
        this.isHighlighted = this.isHighlighted.bind(this);
        this.setHighlighted = this.setHighlighted.bind(this);
        this.isInScope = this.isInScope.bind(this);
        this.setInScope = this.setInScope.bind(this);
    }

    setWidth(newWidth) {
        this.state.width = newWidth;
    }

    isInScope() {
        return this.state.inScope;
    }

    setInScope(inScope) {
        this.state.inScope = inScope;
    }

    isHighlighted() {
        return this.state.highlighted;
    }

    setHighlighted(highlighted) {
        this.state.highlighted = highlighted;
    }

    render() {
        let {content, row, col} = this.props;
        let onClick = this.onClick;
        let {width} = this.state;

        let allClasses = CLASSES.ROW + row + " "
            + CLASSES.COL + col + " "
            + CLASSES.WIDTH + width;

        allClasses += " " + (this.isInScope() ? CLASSES.IN_SCOPE : CLASSES.NOT_IN_SCOPE);
        allClasses += " " + (this.isHighlighted() ? CLASSES.HIGHLIGHTED : CLASSES.NOT_HIGHLIGHTED);

        if (onClick) {
            return (
                <button className={allClasses} onClick={() => {onClick();}}>
                {content}
                </button>
            );
        }
        return (
            <button className={allClasses}>
            {content}
            </button>
        );
    }
}

export default Button;
