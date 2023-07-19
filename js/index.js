const axios = require('axios');
let data = 'USER_FUNCTION_NAME=LOGIN&SYSTEM_FUNCTION_NAME=LOGIN&window=main_eam&userid=MELISSALU&password=!Metr0_linx%23&tenant=DS_MP_1';

let config = {
  method: 'post',
  maxBodyLength: Infinity,
  url: 'https://eam-u2alnxapp.metrolinxuat.com/web/base/login?',
  headers: { 
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 
    'Cookie': 'JSESSIONID=NRpRIira77y05kcRdsV2HwAELGDuUokVha8DZjO1.tomcat01; BIGipServerEAM-U2ALNXAPP-POOL_443=1147910154.47873.0000',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
},
  data : data
};

axios.request(config)
.then((response) => {
  console.log(JSON.stringify(response.data));
})
.catch((error) => {
  console.log(error);
});
