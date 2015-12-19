import React, { Component } from 'react';
import './App.scss';
import moment from 'moment';

export default class ImageItem extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        let image = this.props.image;
        return (
            <tr>
                <td>
                    <a href={image.original_image}>
                        <img height="32" width="32" src={image.original_image}/>
                    </a>
                </td>
                <td>
                    <a href={image.combined}>
                        <img height="32" width="32" src={image.combined}/>
                    </a>
                </td>
                <td>{image.name}</td>
                <td>
                    <span className="label label-info">{image.operator}</span>
                </td>
                <td>{moment(image.date).fromNow()}</td>
            </tr>
        );
    }



}

ImageItem.propTypes = {
    image: React.PropTypes.object.isRequired,
}
