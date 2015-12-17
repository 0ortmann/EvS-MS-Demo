import React, { Component } from 'react';
import FileInputContainer from './FileInputContainer.jsx';
import ImageListContainer from './ImageListContainer.jsx';
import './App.scss';


export class App extends Component {

    render() {
        return (
            <div className='app'>
                <ImageListContainer />
                <FileInputContainer />
            </div>);
    }
}
