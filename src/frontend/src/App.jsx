import React, { Component } from 'react';
import FileInputContainer from './FileInputContainer.jsx';
import ImageListContainer from './ImageListContainer.jsx';
import Login from './Login.jsx';
import request from 'superagent';
import './App.scss';


export class App extends Component {

    constructor(props) {
        super(props);
        this.state = { images: [], token: null };

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

    handleLogin(token) {
        this.setState({token: token});
    }

    handleLogout() {
        this.setState({token: null});
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
            <div>
                <nav className="navbar navbar-default navbar-fixed-top">
                    <div className="container">
                        <a className="navbar-brand" href="#">EvS-Demo</a>
                        <Login token={this.state.token} onLogin={this.handleLogin.bind(this)} onLogout={this.handleLogout.bind(this)}/>
                    </div>
                </nav>
                <div className="container">
                    <div className="row">
                        <ImageListContainer images={this.state.images}/>
                        <FileInputContainer token={this.state.token} handleImageAdded={this.handleImageAdded.bind(this)}/>
                    </div>
                </div>
            </div>);
    }
}
