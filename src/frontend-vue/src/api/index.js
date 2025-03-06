import axios from 'axios'
import { saveAs } from 'file-saver';

export async function get(url, params = {}) {

  let value;

  await axios.get(
    url, 
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

export async function post(url, data = {}, isGetExcel = false) {

  let value;
  
  // if(isGetExcel) {
  //   var headers = {
  //     'Content-Type':'application/x-www-form-urlencoded',
  //     'X-CSRFToken' : await getToken(),
  //     'responseType': 'arraybuffer'
  //   }
  // } else {
    var headers = {
      'Content-Type':'application/x-www-form-urlencoded',
      'X-CSRFToken' : await getToken()
    }
  // }

  var config = {headers: headers}

  await axios.post(
    url,
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

export async function post_file(url, data = {}) {

  let value;

  var headers = {
    'Content-Type':'multipart/form-data',
    'X-CSRFToken' : await getToken()
  }

  var config = {headers: headers}

  await axios.post(
    url,
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

export async function post_get_excel(url, data = {}) {

  let value;
  
  var headers = {
    'X-CSRFToken' : await getToken(),
    // 'responseType': 'arraybuffer'
  }

  var config = {
    headers: headers,
    'responseType': 'arraybuffer'
  }

  await axios.post(
    url,
    data,
    config
  )
  .then((res) => {
    console.log(res)
     // 2.获取文件名称
     const contentDisposition = res.headers.get('content-disposition')
     const fileNameRegexp = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
     const matches = fileNameRegexp.exec(contentDisposition);
     const filename = (matches != null && matches[1] ? decodeURIComponent(matches[1].replace(/['"]/g, '')) : 'unknown');

     // 2.导出到本地保存
     const blob = new Blob([res.data], {type: 'application/vnd.ms-excel'});

     saveAs(blob, filename);

     value = {
        status: true,
        message: '导出成功'
     }
  })
  .catch((error) => {
    console.log(error)
    value = error
  })

  return value;
}

async function getToken() {
  const value = await get('/api/get_token/')
  if (value.status == true) {
    // window.sessionStorage.setItem("csrf_token", value['data'])
    return value['data']
  }
  return null
}
