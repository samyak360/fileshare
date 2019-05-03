var body = document.getElementById("randcolor");

function setGradientRand() {
  setTimeout(setGradientRand,10000);
  var letters = '0123456789ABCDEF';
    var color = '#';
    var color0 = '#';
    for (var i = 0; i < 6; i++) {
    color += letters[Math.floor((Math.random() * 200)%16)];
    color0 += letters[Math.floor((Math.random() * 200)%16)];
    }
  body.style.background = 
  "linear-gradient(to right, " 
  + color
  + ", " 
  + color0
  + ")";

}

let dropArea = document.getElementById('drop-area')

;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false)
})

function preventDefaults (e) {
  e.preventDefault()
  e.stopPropagation()
}

;['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false)
})

;['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false)
})

function highlight(e) {
  dropArea.classList.add('highlight')
}

function unhighlight(e) {
  dropArea.classList.remove('highlight')
}

dropArea.addEventListener('drop', handleDrop, false)

function handleDrop(e) {
  let dt = e.dataTransfer
  let files = dt.files

  handleFiles(files)
}

function handleFiles(files) {
  files = [...files]
  files.forEach(uploadFile)
  files.forEach(previewFile)
}


function uploadFile(file) {
  let url = 'fileshare.py'
  let formData = new FormData()

  formData.append('file', file)

  fetch(url, {
    method: 'POST',
    body: formData
  })
  .then(() => { console.log("upload done"); })
  .catch(() => { console.log("upload failed"); })
}


function previewFile(file) {
  let reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onloadend = function() {
    let img = document.createElement('img')
    img.src = reader.result
    document.getElementById('gallery').appendChild(img)
  }
}

function areachange() {
    let x = document.querySelector('.maindiv');
    let y = document.getElementById('drop-area1');
    x.style.display = "none" 
    y.style.display = "block";
}

setGradientRand();



