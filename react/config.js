
if(process.env.NODE_ENV !== 'production'){
  var BASE_URL = "http://127.0.0.1:1337/" //change your server for your own
}else{
  var BASE_URL = "/"
}

export {BASE_URL}
