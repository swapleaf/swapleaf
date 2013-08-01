var USA_STATES =  [["AL","Alabama"],["AK","Alaska"],["AZ","Arizona"],["AR","Arkansas"],["CA","California"],
   ["CO","Colorado"],["CT","Connecticut"],["DE","Delaware"],["FL","Florida"],["GA","Georgia"],
   ["HI","Hawaii"],["ID","Idaho"],["IL","Illinois"],["IN","Indiana"],["IA","Iowa"],
   ["KS","Kansas"],["KY","Kentucky"],["LA","Louisana"],["ME","Maine"],["MD","Maryland"],
   ["MA","Massachusetts"],["MI","Michigan"],["MN","Minnesota"],["MS","Mississippi"],["MO","Missouri"],
   ["MT","Montana"],["NE","Nebraska"],["NV","Nevada"],["NH","New Hampshire"],["NJ","New Jersey"],
   ["NM","New Mexico"],["NY","New York"],["NC","North Carolina"],["ND","North Dakota"],["OH","Ohio"],
   ["OK","Oklahoma"],["OR","Oregon"],["PA","Pennsylvania"],["RI","Rhode Island"],["SC","South Carolina"],
   ["SD","South Dakota"],["TN","Tennessee"],["TX","Texas"],["UT","Utah"],["VT","Vermont"],
   ["VA","Virginia"],["WA","Washington"],["WV","West Virginia"],["WI","Wisconsin"],["WY","Wyoming"]]

var month = []

var month_name_short = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }

var month_name_full = {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 
            7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        }

var week_day_text = {
          "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", 
          "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"
        }

var week_day_num = {
          0: "Monday", 1: "Tuesday", 2: "Wednesday", 
          3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"
        }

var hour = ["7am",'8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm']

var hour_dict = {
      "7am": 7,'8am': 8,'9am': 9,'10am': 10,'11am': 11,'12pm': 12,'1pm': 13,'2pm': 14,'3pm':15,'4pm':16,'5pm':17,'6pm':18,'7pm':19,'8pm':20,'9pm':21,'10pm':22
}

var minute = ['00','05','10','15','20','25','30','35','40','45','50','55']

var day_per_month = {
            1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9: 30, 10:31,11:30,12:31
}

var USA_STATES_OPTION = "";
for (var i = 0; i < USA_STATES.length; i++) {
	USA_STATES_OPTION = USA_STATES_OPTION + "<option value='" + USA_STATES[i][0] + "'>" + USA_STATES[i][1] + "</option>"		
}

function show_message(data,el) {
    var new_item = $(data).hide();
    $(el).append(new_item);
    new_item.slideDown();
    setTimeout(function(){
        new_item.slideUp(function(){ 
            jQuery(this).remove(); 
        });
    },3000);
}

function is_numeric(el_check) {
    var temp=parseInt($(el_check).val());
    if (isNaN(temp)) {
        return false
    } else {
        return true
    }
    
}

function is_empty(el_check) {
    if(($(el_check).val().length==0) || ($(el_check).val()==null)) {
        return true;
    } else{
        return false
    }
}

function convert_24hr_to_AM_PM(hour,minute){
    var minute_str = minute.toString();
    if (minute < 10){
        minute_str = "0" + minute.toString();
  }
    if (hour == 0) 
        return "12" + ":" + minute_str+ "am";
    if ((hour > 0) && (hour < 12))
        return hour.toString() + ":" + minute_str + "am";
    if (hour == 12) 
        return "12" + ":" + minute_str + "pm";
    if (hour > 12)
        return (hour-12).toString() + ":" + minute_str + "pm";
}