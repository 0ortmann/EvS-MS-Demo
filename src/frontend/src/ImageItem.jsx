import React, { Component } from 'react';

import './App.scss';

export default class ImageItem extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <li className='imageItem'>
                <span>{this.props.name}</span>
            </li>
        );
    }



}

ImageItem.propTypes = {
    name: React.PropTypes.string.isRequired,
}