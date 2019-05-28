import React from 'react'
import 'bootstrap/dist/css/bootstrap.css'

import Header from './Header'
import Body from './Body'
import Footer from './Footer'


export default class App extends React.Component {
	render() {
		return (
			<React.Fragment>
				<Header />
				<Body />
				<Footer />
			</React.Fragment>
		)
	}
}