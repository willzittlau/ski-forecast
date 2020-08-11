// Change Danger rating colour for each day
$(document).ready(function(){
    $('#day1 td.danger').each(function(){
        if ($(this).text() == ' 5:Extreme ') {
            $(this).css('background-color','black');
            $(this).css('color','white');
        }
        else if ($(this).text() == ' 4:High ') {
            $(this).css('background-color','red');
        }
        else if ($(this).text() == ' 3:Considerable ') {
            $(this).css('background-color','orange');
        }
        else if ($(this).text() == ' 2:Moderate ') {
            $(this).css('background-color','yellow');
        }
        else if ($(this).text() == ' 1:Low ') {
            $(this).css('background-color','green');
        }
    });
});

$(document).ready(function(){
    $('#day2 td.danger').each(function(){
        if ($(this).text() == ' 5:Extreme ') {
            $(this).css('background-color','black');
            $(this).css('color','white');
        }
        else if ($(this).text() == ' 4:High ') {
            $(this).css('background-color','red');
        }
        else if ($(this).text() == ' 3:Considerable ') {
            $(this).css('background-color','orange');
        }
        else if ($(this).text() == ' 2:Moderate ') {
            $(this).css('background-color','yellow');
        }
        else if ($(this).text() == ' 1:Low ') {
            $(this).css('background-color','green');
        }
    });
});

$(document).ready(function(){
    $('#day3 td.danger').each(function(){
        if ($(this).text() == ' 5:Extreme ') {
            $(this).css('background-color','black');
            $(this).css('color','white');
        }
        else if ($(this).text() == ' 4:High ') {
            $(this).css('background-color','red');
        }
        else if ($(this).text() == ' 3:Considerable ') {
            $(this).css('background-color','orange');
        }
        else if ($(this).text() == ' 2:Moderate ') {
            $(this).css('background-color','yellow');
        }
        else if ($(this).text() == ' 1:Low ') {
            $(this).css('background-color','green');
        }
    });
});

// Change Elevation color
$(document).ready(function(){
    $('#day1 td.elev').each(function(){
        if ($(this).text() == ' Alpine ') {
            $(this).css('background-color','AliceBlue');
        }
        else if ($(this).text() == ' Treeline ') {
            $(this).css('background-color','#c1d831');
        }
        else if ($(this).text() == ' Below Treeline ') {
            $(this).css('background-color','SeaGreen');
        }
    });
});

$(document).ready(function(){
    $('#day2 td.elev').each(function(){
        if ($(this).text() == ' Alpine ') {
            $(this).css('background-color','AliceBlue');
        }
        else if ($(this).text() == ' Treeline ') {
            $(this).css('background-color','#c1d831');
        }
        else if ($(this).text() == ' Below Treeline ') {
            $(this).css('background-color','SeaGreen');
        }
    });
});

$(document).ready(function(){
    $('#day3 td.elev').each(function(){
        if ($(this).text() == ' Alpine ') {
            $(this).css('background-color','AliceBlue');
        }
        else if ($(this).text() == ' Treeline ') {
            $(this).css('background-color','#c1d831');
        }
        else if ($(this).text() == ' Below Treeline ') {
            $(this).css('background-color','SeaGreen');
        }
    });
});