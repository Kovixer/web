import React from 'react'

import { getPost } from '../func/methods'

import Editor from './Editor'


export default class Main extends React.Component {
	state = {
		posts: [],
	}

	componentWillMount() {
		getPost(this)
	}

	render() {
		return (
			<div>
				{ this.state.posts.map((el, num) => 
					<div key={ num }>{ el.cont }</div>
				) }
				<Editor />
			</div>
		)
	}
}