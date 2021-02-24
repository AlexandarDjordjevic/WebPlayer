
function add_stream(){
    var new_stream_name = document.getElementById('new_stream_name').value;
    var new_stream_url = document.getElementById('new_stream_url').value;
    var new_stream_genre = document.getElementById('new_stream_genre').value;

    var xhttp = new XMLHttpRequest();
    var url = "/add_stream";
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('content-type', "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify({ "name" : new_stream_name, "url" : new_stream_url, "genre" : new_stream_genre }));

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4){
            if(this.status == 200) {
                document.getElementById('new_stream_name').value = "";
                document.getElementById('new_stream_url').value = "";
                document.getElementById('new_stream_genre').value = "";
                get_playlist(update_playlist_table);
                $('#playlistModal').modal('show');        
            }else{
                $('#addToPlaylist').modal('show');
            }
        }

    }
}

function play_stream(stream_url){
    var xhttp = new XMLHttpRequest();
    var url = "/play";
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('content-type', "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify({ "url" : stream_url }));
}

function remove_item(stream_url){
    var xhttp = new XMLHttpRequest();
    var url = "/remove";
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('content-type', "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify({ "url" : stream_url }));
    get_playlist(update_playlist_table);
}

var eq_timer = setInterval(function(){
    if ($("#audio_visual").attr("status") == "play"){
        $('.eqitem').each(function(){
            $(this).height(Math.floor(Math.random() * 90) + 10 );
        });
    }else{
        $('.eqitem').each(function(){
            $(this).height( 20 );
        });
    }
    
}, 200);

var artist_timer = setInterval(current_playing, 2000);
var date_timer = setInterval(refresh_time, 1000);
var volume = document.getElementById("volume");
var mute = document.getElementById("mute") ;
var unmute = document.getElementById("unmute") ;

mute.onclick = function(){
    set_volume(volume.value, false);
}

unmute.onclick = function(){
    set_volume(volume.value, true);
}

volume.oninput = function() {
    set_volume(this.value, false);
}

$(".clickable-row").click(function() {
    window.location = $(this).data("href");
});

function stop(){
    var xmlhttp = new XMLHttpRequest();
    var url = "/stop";
    xmlhttp.open("POST", url, true);
    xmlhttp.send();               
}

function set_volume(volume, mute){
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.open("POST", "set_volume", true);
    xhttp.setRequestHeader('content-type', "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify({ "volume" : volume, "mute" : mute }));
}

function refresh_time(){
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('time_and_date').innerHTML =
        h + ":" + m + ":" + s;
}
function checkTime(i) {
    if (i < 10) {
        i = "0" + i
    }; // add zero in front of numbers < 10
    return i;
}

function current_playing()
{
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data_json = JSON.parse(this.responseText);
            document.getElementById('radio').innerHTML = data_json['station_name'];
            document.getElementById('artist').innerHTML = data_json['current_track']; 
            document.getElementById('audio_visual').setAttribute("status", data_json['status'])                
        }

    }
    xhttp.open("GET", "current_playing", true);
    xhttp.send();
}

// function startTime() {
//     var today = new Date();
//     var h = today.getHours();
//     var m = today.getMinutes();
//     var s = today.getSeconds();
//     m = checkTime(m);
//     s = checkTime(s);
//     document.getElementById('datetime').innerHTML =
//         h + ":" + m + ":" + s;
//     var t = setTimeout(startTime, 500);
// }

// function checkTime(i) {
//     if (i < 10) {
//         i = "0" + i
//     }; // add zero in front of numbers < 10
//     return i;
// }

function update_playlist_table(streams){
    var table = document.getElementById("playlist");
    var tableBody = table.getElementsByTagName('tbody')[0];
    tableBody.innerHTML = "";
    var i;
    for(i = 0; i < streams.length; i++) {
        var row = tableBody.insertRow();
        row.setAttribute("class", "clickable-row");
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        // var cell5 = row.insertCell(4);
        cell1.innerHTML = streams[i].name;
        cell2.innerHTML = streams[i].genre;
        cell3.innerHTML = '<i class="fas fa-play" onclick="play_stream(\'' + streams[i].url + '\')"></i>';
        cell4.innerHTML = '<i class="fa fa-trash" onclick="remove_item(\'' + streams[i].url + '\')"></i>'
        // cell5.innerHTML = '<i class="fa fa-edit"  data-dismiss="modal" data-toggle="modal" data-target="#editPlayistItem"></i>'
    }
}

function get_playlist(callback){
    var xmlhttp = new XMLHttpRequest();
    var url = "/get_playlist";
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var streams = JSON.parse(this.responseText);
            callback(streams);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function testMe(){
    var xmlhttp = new XMLHttpRequest();
    var url = "/get_paired_devices";
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var myArr = JSON.parse(this.responseText);
            myFunction(myArr);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

    
function myFunction(arr) {
    var table = document.getElementById("paired");
    var i;
    for(i = 0; i < arr.length; i++) {
        var row = table.insertRow(1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        cell1.innerHTML = arr[i].name;
        cell2.innerHTML = arr[i].mac_address;
        cell3.innerHTML = '<button type="button" class="btn btn-outline-info btn-sm">Connect</button>';
    }
}