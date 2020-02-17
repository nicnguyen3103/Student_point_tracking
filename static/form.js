function reload () { 
    location.reload();}

document.addEventListener('DOMContentLoaded', function(event) {
    var submitButton = document.getElementById("submit")
    submitButton.addEventListener("click",ajax_form_submit);
    
    function ajax_form_submit(){
        console.log("testing ajax");
        student_rows = document.getElementsByClassName("student_row");
        var arrayLength = student_rows.length;
        student_datas = [];
        for (var i = 0; i < arrayLength; i++) {
            var id=document.getElementsByClassName("student_id")[i].value;
            var activity=document.getElementsByClassName("student_activity")[i].value;
            var point =document.getElementsByClassName("student_point")[i].value;
            var checkin = document.getElementsByClassName("student_checkin")[i].checked;
            student_datas.push(
                {"id": id,
                "activity":activity,
                "point": point,
                "checkin": checkin
                }
            )
        }
        console.log(student_datas);
        fetch('/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(student_datas)
            }).then(res=>res.json())
            .then(res => {
                console.log(res);
                if (res.success == true){
                    console.log ("clear function");
                    reload();
                }
            });
        
    }

})

