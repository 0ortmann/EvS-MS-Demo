import React, { Component } from 'react';
import ImageItem from './ImageItem.jsx'
import './App.scss';

export default class ImageListContainer extends Component {

    render() {
        let images = this.props.images;
        if(images.length === 0) {
            return (<div className='images'><h3>Keine Bilder</h3></div>);
        }

        let _this = this;
        return (
            <div className="col-md-7">
                <h2>Images</h2>
                <table className='table imageItemList'>
                    <thead>
                        <tr>
                            <th>Orig.</th>
                            <th>Comb.</th>
                            <th>Image name</th>
                            <th>Operator</th>
                            <th>Posted</th>
                        </tr>
                    </thead>
                    <tbody>
                        {images.map(function(item) {
                            return <ImageItem image={item}/>
                        })}
                    </tbody>
                </table>
            </div>);
    }
}
