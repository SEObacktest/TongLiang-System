import axios from 'axios'

import { URL } from './config';

export async function get(url:string, params = {}) {

  let value;

  await axios.get(
    URL + url, 
    params,
  )
  .then((response) => {
    value = response.data
  })
  .catch((error) => {
    console.log(error)
    value = error
  })

  return value;

}

export async function post(url:string, data = {}) {

  let value;
  
  var headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'X-CSRFToken' : await getToken()
  }
  var config = {headers: headers}

  await axios.post(
    URL + url,
    data,
    config
  )
  .then((response) => {
    value = response.data
  })
  .catch((error) => {
    console.log(error)
    value = error
  })

  return value;
}

export async function post_file(url:string, data = {}) {

  let value;

  var headers = {
    'Content-Type':'multipart/form-data',
    'X-CSRFToken' : await getToken()
  }

  var config = {headers: headers}

  await axios.post(
    URL + url,
    data,
    config
  )
  .then((response) => {
    value = response.data
  })
  .catch((error) => {
    console.log(error)
    value = error
  })

  return value;
}

async function getToken() {
  const value:any = await get('/api/get_token/')
  if (value.status == true) {
    // window.sessionStorage.setItem("csrf_token", value['data'])
    return value['data']
  }
  return null
}