import React, { Component } from 'react';
import ImageItem from './ImageItem.jsx'
import './App.scss';

export default class ImageListContainer extends Component {

    constructor(props) {
        super(props);
        this.state = { images: [] };
    }

    componentDidMount() {
        this.fetchImages();
    }

    fetchImages() {
        let _this = this;
        request.get('http://localhost:1337/images').end(function(err, res) {
            if(err) {
                console.log(err); 
            }
            _this.setState({images: JSON.parse(res.text)});
            //console.log(_this.state.images);
        });
    }

    render() {

        let images = this.state.images;
        if(images.length === 0) {
            return (<div className='images'><h3>Keine Bilder</h3></div>);
        }

        let _this = this;
        return (
            <div className='imageListContainer'>
                <h3>Bilder</h3>
                <ul className='imageItemList'>
                {images.map(function(item) {
                    return <ImageItem name={item.name} amount={item.amount} date={item.date} deleteCB={_this.deleteExpense}/>
                })}
                </ul>
            </div>);
    }
}
