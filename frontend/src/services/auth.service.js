import axios from 'axios';
import authHeader from './auth-header';
import { API_URL } from './api'

class AuthService {
  login(user) {
    var formdata = new FormData();
    formdata.append("username", user.username);
    formdata.append("password", user.password);
    return axios
      .post(API_URL + 'auth/token', formdata,
      {headers:{'Content-Type' : 'application/json'}}
      )
      .then(response => {
        if (response.data.access_token) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('user');
  }

  googlelogin(token) {
    return axios
      .post(API_URL + 'auth/google', {
        tokenstr: token,
      },
      {headers:{'Content-Type' : 'application/json'}}
      )
      .then(response => {
        if (response.data.access_token) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  validateToken() {
    return axios.get(API_URL + 'auth/validate', { headers: authHeader() });
  }

  refreshToken() {
    let user = JSON.parse(localStorage.getItem('user'));
    return axios.post(
      API_URL + 'auth/refresh',
      {'refresh_token': user.refresh_token}
    )
    .then(response => {
      if (response.data.access_token) {
        localStorage.setItem('user', JSON.stringify(response.data));
      }

      return response.data;
    })
  }

  register(user) {
    return axios.post(API_URL + 'users/create', {
      username: user.username,
      email: user.email,
      hashed_password: user.password,
      full_name: user.full_name
    });
  }
}

export default new AuthService();
