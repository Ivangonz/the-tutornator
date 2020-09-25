// import Home from './components/Home.vue'
import Portfolio from './components/portfolio/Portfolio.vue'
import Stocks from './components/stocks/Stocks.vue'
import Login from './components/public/Login.vue'
import Secure from './components/secure/Secure.vue'


export const routes = [
  {path: '/', component: Login, name: 'login'},
  {path: '/portfolio', component: Portfolio, name: 'portfolio'},
  {path: '/stocks', component: Stocks, name: 'stocks'},
  // {path: '/login', component: Login, name: 'login'},
  {path: '/secure', component: Secure, name: 'secure'}
];