const work = document.getElementsByClassName('work')[0];
const ajaxLink = document.getElementsByClassName('ajax_link')[0];
const mainLink = document.getElementsByClassName('active_link_text')[0];
const title = document.querySelectorAll('title')[0];
const refreshButton = document.getElementsByClassName('refreshButton')[0];

ajaxLink.addEventListener('click', toDbPage);
refreshButton.addEventListener('mousedown', longClick)
refreshButton.addEventListener('click', refreshDB)


let btnActive, video, canvas, df, errorText, errorText2, toDbButton, toDbDiv, preButton, nextButton

function addListeners() {

  btnActive = document.getElementsByClassName('dButton Active')[0];
  video = document.querySelector('video'); 
  canvas = document.getElementsByClassName('canvas')[0];
  df = document.getElementsByClassName('downloadForm')[0];
  errorText = document.getElementsByClassName('errorText')[0];
  errorText2 = document.getElementsByClassName('errorText2')[0];
  toDbDiv = document.getElementsByClassName('toDbDiv')[0];

  btnActive.addEventListener('click', change_flag);
}

function addListenersToDB() {
  nextButton = document.getElementsByClassName('secondButton')[0];
  nextButton.addEventListener('click', next_viborka);

  preButton = document.getElementsByClassName('firstButton')[0];
  preButton.addEventListener('click', pre_viborka);
}

addListeners();

let flag = false;
let to_screen_counter = '0';
let to_cam_counter = '0';
let coord_x = '0';
let coord_y = '0';
let coord_w = '10';
let coord_h ='10';
let result = 'to_screen';
let db_flag = false;
let save_counter = 0;
let db_success = null;
let main_page = work.innerHTML;
let db_counter = 0;


function longClick() {
  refreshButton.className = "refreshButtonLClick";
}


function refreshDB() {
  refreshButton.className = "refreshButton";
  $.ajax({
    url: '/download/refresh=true',
    type: 'get',
    success: function(response) {
      window.location.href = '/'
    },
    dataType: 'json'
  });
}


function toDB() {
  db_flag = true;
  save_counter += 1;
}



function toDbPage() {
  stopStream();
  title.innerHTML = 'База данных';
  mainLink.className = 'ajax_link';
  ajaxLink.className = 'active_link_text';

  btnActive.removeEventListener('click', change_flag);
  getPage();
  mainLink.addEventListener('click', toMainPage);
}

function toMainPage() {
  title.innerHTML = 'Начать работу';
  mainLink.removeEventListener('click', toMainPage);
  nextButton.removeEventListener('click', next_viborka)
  preButton.removeEventListener('click', pre_viborka)
  mainLink.className = 'active_link_text'
  ajaxLink.className = 'ajax_link'
  work.innerHTML = main_page;
  addListeners();
  db_counter = 0;
}


function stopStream() {
  flag = false;
  if (toDbButton) {
    toDbButton.removeEventListener('click', toDB)
  }
  toDbDiv.innerHTML = '';
  setTimeout(() => {
  if (typeof(video_track) != 'undefined') {
    video_track.stop();
  }
  btnActive.innerText = 'Начать';
  df.innerHTML = '<canvas class="canvas2"></canvas>';
  errorText.innerHTML = '';
  counter = 0;
  average_fps = 0;
}
  , 100);  
}

function getPage() {
  $.ajax({
    url: '/download',
    type: 'get',
    data: {"type": "get_db_page",
            "db_counter": db_counter},
    success: function(response) {
      makePage(response);
    },
    dataType: 'json'
  });
}

function makePage(response) {
  work.innerHTML = response.text;
  if (response.total == 0) {
    nextButton = document.getElementsByClassName('secondButton')[0];
    preButton = document.getElementsByClassName('firstButton')[0];

    preButton.className = 'firstButton_Passive';
    nextButton.className = 'secondButton_Passive'
  }
  else if (response.first_in_table <= 10 && response.total > 10) {
    nextButton = document.getElementsByClassName('secondButton')[0];
    preButton = document.getElementsByClassName('firstButton')[0];

    preButton.className = 'firstButton';
    nextButton.className = 'secondButton_Passive'
   
    preButton.addEventListener('click', pre_viborka);
  }
  else if (response.first_in_table <= 10 && response.total <= 10) {
    nextButton = document.getElementsByClassName('secondButton')[0];
    preButton = document.getElementsByClassName('firstButton')[0];

    preButton.className = 'firstButton_Passive';
    nextButton.className = 'secondButton_Passive'
  }
  else if (response.first_in_table == response.total) {
    nextButton = document.getElementsByClassName('secondButton')[0];
    preButton = document.getElementsByClassName('firstButton')[0];

    preButton.className = 'firstButton_Passive';
    nextButton.className = 'secondButton'

    nextButton.addEventListener('click', next_viborka);
  } 
  else {
    addListenersToDB();
  }
}


function next_viborka() {
  db_counter += 10;
  getPage();
}

function pre_viborka() {
  db_counter -= 10;
  getPage();
}


let average_fps = 0;
let counter = 0;
let time_temp = 0;
let timeout_flag = false;

function change_flag() {
  if (flag == false) {
    btnActive.innerText = 'Остановить';
    var canvas2 = document.getElementsByClassName('canvas2')[0];
    flag = true;
    if(navigator.webkitGetUserMedia!=null) { 
        var options = { 
          'video':true 
        }; 
        
        // запрашиваем доступ к веб-камере
        navigator.webkitGetUserMedia(options, 
          async function(stream) { 

            toDbDiv.innerHTML = '<div class="toDB"><p>Сохранить в БД</p></div>'
            toDbButton = document.getElementsByClassName('toDB')[0];
            toDbButton.addEventListener('click', toDB);

            window.localStream = stream;
            video_track = localStream.getVideoTracks()[0];
            const imageCapture = new ImageCapture(video_track);

            frame = await imageCapture.grabFrame();

            var ctx = canvas.getContext('2d');
            canvas.height = frame.height;
            canvas.width = frame.width;

            var ctx2 = canvas2.getContext('2d');
            canvas2.height = frame.height;
            canvas2.width = frame.width;


            while (flag == true) {
              counter += 1;
              const start = new Date().getTime();

              frame = await imageCapture.grabFrame();
              ctx.drawImage(frame, 0, 0)
              dataURL = canvas.toDataURL();

              var formData = new FormData();
              formData.append('image', dataURL);
              formData.append('to_screen_counter', to_screen_counter);
              formData.append('to_cam_counter', to_cam_counter);
              formData.append('coord_x', coord_x);
              formData.append('coord_y', coord_y);
              formData.append('coord_w', coord_w);
              formData.append('coord_h', coord_h);
              formData.append('save_to_db', db_flag);
              formData.append('save_counter', save_counter);
              

              $.ajax({
                url: '/download',
                type: 'post',
                cache: false,
                contentType: false,
                processData: false,
                dataType: 'json',
                data: formData,
                success: function(response) {
                    if (response.type == "error") {
                      console.log(response.text);
                    }
                    else {
                      to_screen_counter = response.to_screen_counter;  
                      to_cam_counter = response.to_cam_counter;
                      coord_h = response.coord_h;
                      coord_w = response.coord_w;
                      coord_x = response.coord_x;
                      coord_y = response.coord_y;
                      result = response.result;
                      if (db_flag == true) {
                        db_success = response.db_success;
                      }
                      var img = new Image;
                      img.onload = function(){
                        ctx2.drawImage(img,0,0);
                      };
                      img.src = response.text;
                    }
                }
              })
              const end = new Date().getTime();
              fps = (1/((end - start)/1000)).toFixed(2);
              average_fps += parseFloat(fps);
              if (result == 'to_screen') {
                if (to_screen_counter == 3) {
                  time_temp = 0;
                }
                else {
                  time_temp += (end - start) / 1000;
                }
                errorText.innerHTML = `<p>FPS: ${fps}</p><p>Средний: ${(average_fps/counter).toFixed(2)}</p><p>Взгляд: в экран ${time_temp.toFixed(1)} секунд</p>`;
              }
              else {
                if (to_cam_counter == 2) {
                  time_temp = 0;
                }
                else {
                  time_temp += (end - start) / 1000;
                }
                errorText.innerHTML = `<p>FPS: ${fps}</p><p>Средний: ${(average_fps/counter).toFixed(2)}</p><p>Взгляд: <span class="toGreen">в камеру ${time_temp.toFixed(1)} секунд</span></p>`;
              }
              if (db_flag == true) {
                if (db_success == 'true') {
                  errorText2.innerHTML = `<span class="toGreen">Загружено успешно (${save_counter})</span>`;
                  if (timeout_flag == false) {
                    timeout_flag = true;
                    setTimeout(() => {
                      errorText2.innerHTML = '';
                      timeout_flag = false;
                    }, 1000);
                  }
                }
                else {
                  errorText2.innerHTML = `<span class="toGreen">Загружено успешно (${save_counter})</span>`;
                  if (timeout_flag == false) {
                    timeout_flag = true;
                    setTimeout(() => {
                      errorText2.innerHTML = '';
                      timeout_flag = false;
                    }, 1000);
                  }
                  // errorText2.innerHTML = '<span>Ошибка загрузки</span>'
                }
              }
              db_flag = false;
            }
          }, 
          function(e) { 
            console.log("error happened"); 
          } 
        ); 
      }
  } 
  else {
    stopStream();
  }
}
