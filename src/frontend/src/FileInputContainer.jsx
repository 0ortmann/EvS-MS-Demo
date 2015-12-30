import React, { Component } from 'react';
import request from 'superagent';
import './App.scss';

export default class FileInputContainer extends Component {

    constructor(props) {
        super(props);
        this.state = { operator: 'roberts_cross', files: null }; // hacky init state.
    }

    handleOperatorChange(e) {
        this.setState({operator: e.target.value});
    }

    handleFileChange(e) {
        this.state.files = e.target.files;
    }

    handleSubmit(e) {
        e.preventDefault();
        console.log(this.state);
        if (this.state.files) {
            let files = this.state.files;
            for (let i = 0; i < files.length; i++) {
                let file = files[i];
                this.props.handleImageAdded({
                    name: file.name,
                    operator: this.state.operator,
                    date: (new Date()).getTime(),
                    original_image: URL.createObjectURL(file)
                });
                request
                    .post('http://localhost:1338/process/' + this.state.operator)
                    .attach('file', file, file.name)
                    .end(function (err, res) {
                        if (err) {
                            console.log(err);
                        }
                    });
            }
        }
    }

    render() {
        return (
            <div className="col-md-5">
                <h2>Upload an image</h2>
                <form onSubmit={this.handleSubmit.bind(this)}>
                    <div className="form-group">
                        <label htmlFor="selectOperator">Edge detection operator</label>
                        <select type="file" id="selectOperator" className="form-control" onChange={this.handleOperatorChange.bind(this)} value={this.state.operator}>
                            <option value="roberts_cross">Robert's Cross</option>
                            <option value="prewitt">Prewitt</option>
                            <option value="sobel">Sobel</option>
                            <option value="scharr">Scharr</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="inputFile">Image file</label>
                        <input type="file" id="inputFile" accept="image/png" name="file" onChange={this.handleFileChange.bind(this)}/>
                    </div>

                    <div className="form-group">
                        <button type="submit" className="btn btn-primary">Submit</button>
                    </div>
                </form>
            </div>);
    }
}
