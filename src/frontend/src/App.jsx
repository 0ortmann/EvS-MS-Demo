import React, { Component } from 'react';
import FileInputContainer from './FileInputContainer.jsx';
import ImageListContainer from './ImageListContainer.jsx';
import request from 'superagent';
import './App.scss';


export class App extends Component {

    constructor(props) {
        super(props);
        this.state = { images: [] };

        let _this = this;
        window.setInterval(function () {
            _this.fetchImages();
        }, 10000);
    }

    componentDidMount() {
        this.fetchImages();
    }

    handleImageAdded(image) {
        this.state.images.unshift(image);
        this.setState({images: this.state.images});
    }

    fetchImages() {
        let _this = this;
        request.get('http://localhost:1339/images').end(function(err, res) {
            if(err) {
                console.log(err);
            }
            _this.setState({images: res.body});
            //console.log(_this.state.images);
        });
    }

    render() {
        return (
            <div className='row'>
                <ImageListContainer images={this.state.images}/>
                <FileInputContainer handleImageAdded={this.handleImageAdded.bind(this)}/>
            </div>);
    }
}
