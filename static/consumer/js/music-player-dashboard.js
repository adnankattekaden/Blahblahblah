let now_playing1 = document.querySelector(".now-playing1");
let track_art1 = document.querySelector(".track-art1");
let track_name1 = document.querySelector(".track-name1");
let track_artist1 = document.querySelector(".track-artist1");

let playpause_btn1 = document.querySelector(".playpause-track1");
let next_btn1 = document.querySelector(".next-track1");
let prev_btn1 = document.querySelector(".prev-track1");

let seek_slider1 = document.querySelector(".seek_slider1");
let volume_slider1 = document.querySelector(".volume_slider1");
let curr_time1 = document.querySelector(".current-time1");
let total_duration1 = document.querySelector(".total-duration1");

let track_index1 = 0;
let isPlaying1 = false;
let updateTimer1;

// Create new audio element
let curr_track1 = document.createElement('audio');

// Define the tracks that have to be played
let track_list1 = [
   {
    name: "Pop Smoke",
    artist: "Cascada",
    image: "images/dashboard/audio/01.png",
    path: "images/dashboard/audio/audio.mp3"
  },
  {
    name: "Gabby Barrett",
    artist: "Emeli Sande",
    image: "images/dashboard/audio/01.png",
    path: "images/dashboard/audio/audio.mp3"
  },
  {
    name: "Megan Thee",
    artist: "Jessie J",
    image: "images/dashboard/audio/01.png",
    path: "images/dashboard/audio/audio.mp3",
  },
];

function random_bg_color1() {

  // Get a number between 64 to 256 (for getting lighter colors)
  let red = Math.floor(Math.random() * 256) + 64;
  let green = Math.floor(Math.random() * 256) + 64;
  let blue = Math.floor(Math.random() * 256) + 64;

  // Construct a color withe the given values
  let bgColor = "rgb(" + red + "," + green + "," + blue + ")";

}

function loadTrack(track_index1) {
  clearInterval(updateTimer1);
  resetValues();
  curr_track1.src = track_list1[track_index1].path;
  curr_track1.load();

  if(track_art1)
  {
    track_art1.style.backgroundImage = "url(" + track_list1[track_index1].image + ")";  
  }
  if( track_name1 )
  {
    track_name1.textContent = track_list1[track_index1].name;  
  }

  if(track_artist1)
  {
    track_artist1.textContent = track_list1[track_index1].artist;  
  }
  if(now_playing1)
  {
    now_playing1.textContent = "PLAYING " + (track_index1 + 1) + " OF " + track_list1.length;  
  }
  
  

  updateTimer1 = setInterval(seekUpdate, 1000);
  curr_track1.addEventListener("ended", nextTrack);
  random_bg_color1();
}

function resetValues1() {
  curr_time1.textContent = "00:00";
  total_duration1.textContent = "00:00";
  seek_slider1.value = 0;
}

// Load the first track in the tracklist
loadTrack(track_index1);

function playpauseTrack1() {
  if (!isPlaying1) playTrack1();
  else pauseTrack1();
}

function playTrack1() {
  curr_track1.play();
  isPlaying1 = true;
  playpause_btn1.innerHTML = '<i class="fa fa-pause-circle fa-3x"></i>';
}

function pauseTrack1() {
  curr_track1.pause();
  isPlaying1 = false;
  playpause_btn1.innerHTML = '<i class="fa fa-play-circle fa-3x"></i>';;
}

function nextTrack1() {
  if (track_index1 < track_list1.length - 1)
    track_index1 += 1;
  else track_index1 = 0;
  loadTrack(track_index1);
  playTrack1();
}

function prevTrack1() {
  if (track_index1 > 0)
    track_index1 -= 1;
  else track_index1 = track_list1.length;
  loadTrack(track_index1);
  playTrack1();
}

function seekTo1() {
  seekto = curr_track1.duration * (seek_slider1.value / 100);
  curr_track1.currentTime = seekto;
}

function setVolume1() {
  curr_track1.volume = volume_slider1.value / 100;
}

function seekUpdate1() {
  let seekPosition = 0;

  if (!isNaN(curr_track1.duration)) {
    seekPosition = curr_track1.currentTime * (100 / curr_track1.duration);

    seek_slider1.value = seekPosition;

    let currentMinutes = Math.floor(curr_track1.currentTime / 60);
    let currentSeconds = Math.floor(curr_track1.currentTime - currentMinutes * 60);
    let durationMinutes = Math.floor(curr_track1.duration / 60);
    let durationSeconds = Math.floor(curr_track1.duration - durationMinutes * 60);

    if (currentSeconds < 10) { currentSeconds = "0" + currentSeconds; }
    if (durationSeconds < 10) { durationSeconds = "0" + durationSeconds; }
    if (currentMinutes < 10) { currentMinutes = "0" + currentMinutes; }
    if (durationMinutes < 10) { durationMinutes = "0" + durationMinutes; }

    curr_time1.textContent = currentMinutes + ":" + currentSeconds;
    total_duration1.textContent = durationMinutes + ":" + durationSeconds;
  }
}


