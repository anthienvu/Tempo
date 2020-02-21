function update_display(history_data){
	var history_text = '';
	for (var i = 0; i<history_data.length; i++) {
		var display_text = ''
		if(i>=0){
			history_text = history_text.concat(create_text(history_data[i]));
		};
	};	
	// get previous notes
	document.getElementById("history_note").value = history_text;
	// update time display
	var new_date = new Date();
	var hours = new_date.getHours().toString();
	var minutes = new_date.getMinutes().toString();
	document.getElementById("date").value = new_date.toISOString().substr(0, 19).replace(/T.*/, ' ');
	document.getElementById("time_note").value = hours.concat(":", minutes);
	//reset input note
	document.getElementById("note_input").value = "";

};
function create_text(data) {
	var text_data = '';
	var whiteSpace = '';
	var level = get_obj_value(data, 'level') || 0;
	var obj_time = get_obj_value(data, 'time') || 'NA';
	var value = get_obj_value(data, 'value') || '';
	for(var j= 0; j < level; j++) {
		whiteSpace = whiteSpace.concat('   ');
	};
	text_data = text_data.concat(obj_time,':');
	text_data = text_data.concat(value, '\n');
	text_data = whiteSpace + text_data.split('\n').join(whiteSpace + '\n') ;
	return text_data;
};
function get_obj_value(obj, key){
	if(typeof(obj)==='object' && key in obj){
		return obj[key]
	} else {
		return false
	};
};

function get_storage() {
	return new Promise(function(resolve, reject) {
		chrome.storage.local.get(['history_data'], function(result) {
			if('history_data' in result){
				resolve(result.history_data);
			} else {
				resolve([]);
			};
		});
	});
};
function update(data, display_only=false){
	get_storage().then(function(value) {
		if(!display_only) {
			value.push(data);
		};
		update_display(value);		
		chrome.storage.local.set({'history_data': value});
    });
};

function get_new_date() {
	//get new note value
	var level_e = document.getElementById('level');
	var level = parseInt(level_e.options[level_e.selectedIndex].value);
	var input_note = document.getElementById("note_input").value;
	var time = document.getElementById("time_note").value;
	var date = document.getElementById("date").value;
	//storage note to local memory
	var new_date = {'level':level,'value':input_note, 'time':time, 'date': date};
	return new_date;
};
function closeWin() {
  window.close();   // Closes the new window
  return null;
};

function export_csv() {
	get_storage().then(function(data_tbl) {
		var csv_data = 'data:text/csv,';
		var cur_date = '';
		var create_file = false;
		var file_name = '';
		//create csv data
		while(data_tbl.length > 0){
			if(cur_date===data_tbl[0]['date']){
				line = data_tbl.shift();
				csv_data = csv_data.concat(line['time'],';');
				csv_data = csv_data.concat(line['level'],';');
				csv_data = csv_data.concat(line['value'],';', '\n');
				if(data_tbl.length===0) {
					create_file = true;
					file_name = cur_date.concat('.csv');
				};
			} else {
				if (cur_date!==''){
					create_file = true;
					file_name = cur_date.concat('.csv');										
				};
				cur_date = data_tbl[0]['date'];;
			};
			
			if (create_file){
				//creative new log file
				export_file(csv_data, file_name);
				csv_data = 'data:text/csv,';
				create_file = false;			
			};
		};
	});
};

function export_text() {
	get_storage().then(function(data_tbl) {
		var text_data = 'data:text,';
		var cur_date = '';
		var create_file = false;
		var file_name = '';
		//creative new log file
		while(data_tbl.length > 0){
			if(cur_date===data_tbl[0]['date']){
				line = data_tbl.shift();
				text_data = text_data.concat(create_text(line));
				if(data_tbl.length===0) {
					create_file = true;
					file_name = cur_date.concat('.txt');
				};
			} else {
				if (cur_date!==''){
					create_file = true;
					file_name = cur_date.concat('.txt');										
				};
				cur_date = data_tbl[0]['date'];
			};
			if (create_file){
				alert(file_name);
				//creative new log file
				export_file(text_data, file_name);
				text_data = 'data:text,';
				create_file = false;			
			};
		};
	});
};

function export_file(data,file_name) {
	var link = document.createElement("a");
	link.textContent = "Save as TEXT";
	link.download = file_name;
	link.href = data;
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);
};

update(get_new_date(), true);	

document.addEventListener('DOMContentLoaded', function () {
	document.getElementById('export_csv').addEventListener('click', export_csv);
	document.getElementById('export_text').addEventListener('click', export_text);
	document.getElementById("note_input").addEventListener("keypress",function() {
		//when input 'enter'
		if(event.keyCode == 13 && event.shiftKey){
			update(get_new_date());
			setTimeout(closeWin, 500);
		};
	});
	document.getElementById("timer").addEventListener("keypress",function() {
		// Handle key press
		var key = event.keyCode;
		key = String.fromCharCode(key);
		var regex = /[0-9]/;
		if( !regex.test(key) ) {
		event.returnValue = false;
		if(event.preventDefault) event.preventDefault();
		};
	});
});



