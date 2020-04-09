import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

import './style.css'
import { name } from '../../../sets'


// const sciences = [
// 	'math', 'prog', 'bis', 'manag', 'lead', 'marketing', 'life_safety'
// ]

const events = [
	'hack', 'meet', 'lect', 'pres'
]


export default function Header(props) {
	const { system, online, changeTheme } = props
	const { t } = useTranslation()

	return (
		<nav className={`navbar navbar-expand-lg navbar-${system.theme} bg-${system.theme} sticky-top`}>
			<div className="container">
				<Link to="/" className="navbar-brand"><img src={`/brand/logo_${system.color}.svg`} alt={ name } /></Link>
				<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
					<span className="navbar-toggler-icon"></span>
				</button>

				<div className="collapse navbar-collapse" id="navbarTogglerDemo02">
					<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
						<li className="nav-item">
							<Link to="/" className="nav-link">{ t('structure.space') }</Link>
						</li>
						<li className="nav-item dropdown">
							<Link to="/posts/" className="nav-link">{ t('structure.posts') }</Link>
							{/* <Link to="/admin/add/ladder/"><span className="badge badge-dark">+</span></Link> */}
							{/* <div className="dropdown-content">
								{
									sciences.map((science) => (
										<Link to={ `/posts/${science}/` } data-toggle="tooltip">{ t(`science.${science}`) }</Link>
									))
								}
							</div> */}
						</li>
						<li className="nav-item dropdown">
							<Link to="/events/" className="nav-link">{ t('structure.events') }</Link>
							<div className="dropdown-content">
								{
									events.map((event, ind) => (
										<Link
											to={ `/events/${event}/` }
											data-toggle="tooltip"
											key={ ind }
										>{ t(`events.${event}`) }</Link>
									))
								}
							</div>
						</li>
					</ul>
					<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
						<li className="nav-item dropdown">
							<form action="/search/" method="post" className="form-inline my-2 my-lg-0">
								<input name="search" className="form-control mr-sm-2" type="search" placeholder={ t('system.search') } />
							</form>
						</li>
					</ul>
					<ul className="nav navbar-nav navbar-right">
						<li className="nav-item">
							<div>
								{ online.count ? (
									<>
										{t('system.online')}
										<div className="online"></div>
										<div className="badge badge-secondary">{ online.count } </div>
									</>
								) : (
									<>
										{t('system.offline')}
										<div className="offline"></div>
									</>
								) }
							</div>
						</li>
						<li className="nav-item">
							{system.theme === 'dark' ? (
								<div className="badge" onClick={() => {changeTheme('light')}}>
									<i className="fas fa-sun" />
								</div>
							) : (
								<div className="badge" onClick={() => {changeTheme('dark')}}>
									<i className="fas fa-moon" />
								</div>
							)}
						</li>
						<li className="nav-item">
							{localStorage.getItem('lang') === 'ru' ? (
								<div className="badge" onClick={ () => {props.handlerLang('en')} }>
									<img src="/lang/en.svg" alt="en" />
								</div>
							) : (
								<div className="badge" onClick={ () => {props.handlerLang('ru')} }>
									<img src="/lang/ru.svg" alt="ru" />
								</div>
							)}
						</li>
						<li className="nav-item">
							<Link to="/user/"className="nav-link">@</Link><Link to="/sys_sign_out/" className="nav-link">{ t('system.sign_out') }</Link>
							{/* <Link to="/login/" className="nav-link">Гость &nbsp; { t('system.sign_in') }</Link> */}
						</li>
					</ul>
				</div>
			</div>
		</nav>
	)
}