import React, { Component } from 'react';
import request from 'superagent';
import './App.scss';
import JWT from 'jsonwebtoken';
import $ from 'jquery';

export default class Login extends Component {

    constructor(props) {
        super(props);
        this.state = { name: 'admin', password: '' }; // hacky init state.
    }

    handleNameChange(e) {
        this.setState({name: e.target.value});
    }

    handlePasswordChange(e) {
        this.setState({password: e.target.value});
    }

    handleSubmit(e) {
        e.preventDefault();
        let onLogin = this.props.onLogin;
        this.setState({password: ''});
        request
            .post('http://localhost:1339/login')
            .type('form')
            .set('Accept', 'application/jwt')
            .send({name: this.state.name, password: this.state.password})
            .end(function (err, res) {
                if (err) {
                    console.log(err);
                    return;
                }

                let jwt = res.text;
                onLogin(jwt);
            })
        ;
    }

    handleDropDown(e) {
        e.preventDefault();
        $(e.target).parents(".dropdown").toggleClass('open');
    }

    render() {
        if (this.props.token) {
            let user = JWT.decode(this.props.token);
            return (
                <ul className="nav navbar-nav navbar-right">
                    <li className="dropdown">
                        <a href="#" className="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false" onClick={this.handleDropDown.bind(this)}>
                            {user.given_name} {user.family_name} <span className="caret"/>
                        </a>
                        <ul className="dropdown-menu">
                            <li className="dropdown-header">Given name</li>
                            <li className="disabled"><a href="#">{user.given_name}</a></li>
                            <li role="separator" className="divider"/>
                            <li className="dropdown-header">Family name</li>
                            <li className="disabled"><a href="#">{user.family_name}</a></li>
                            <li role="separator" className="divider"/>
                            <li className="dropdown-header">Gender</li>
                            <li className="disabled"><a href="#">{user.gender}</a></li>
                            <li role="separator" className="divider"/>
                            <li className="dropdown-header">Username</li>
                            <li className="disabled"><a href="#">{user.name}</a></li>
                            <li role="separator" className="divider"/>
                            <li className="dropdown-header">E-Mail</li>
                            <li className="disabled"><a href="#">{user.email}</a></li>
                            <li role="separator" className="divider"/>
                            <li><a href="#" onClick={this.props.onLogout}>Log out</a></li>
                        </ul>
                    </li>
                </ul>
            );
        }

        return (
            <form className="navbar-form navbar-right" onSubmit={this.handleSubmit.bind(this)}>
                <div className="form-group">
                    <input type="text" className="form-control" placeholder="Username" value={this.state.name} onChange={this.handleNameChange.bind(this)}/>
                </div>
                <div className="form-group">
                    <input type="password" className="form-control" placeholder="Password" value={this.state.password} onChange={this.handlePasswordChange.bind(this)}/>
                </div>
                <button type="submit" className="btn btn-default">Login</button>
            </form>);
    }
}
