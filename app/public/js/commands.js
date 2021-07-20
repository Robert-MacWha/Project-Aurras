//? attach the logSubmit function to the forms
$('form').submit(function(e) {
    
    // get the data from the form and json-ify it
    let raw_data = $(this).serializeArray();
    let id = $(this).attr('id');

    let data = {'type': id};
    for (let i = 0; i < raw_data.length; i ++) {
        data[raw_data[i].name] = raw_data[i].value;
    }

    // if the data is from the intents form, manually grab the selected entities since the data returned by serializeArray is wonkey
    if (id == 'intents') {
        data.entities = []
        $('.dropdown-menu.inner .selected .text').each(function(index, element) {
            data.entities.push($(element).text());
        });
    }

    // if the data is from the prompts form, fit any entities it has into a single array
    if (id == 'prompts') {
        data.entities = {}
        for(const [key, value] of Object.entries(data)) {
            if (key.includes('entity-')) {

                data.entities[key.replace('entity-', '')] = value;
                delete data[key];

            }
        }
    }

    // send the data to main
    window.api.request('command_add', data);

});

//? add in search functionality to the bootstrap tables (https://www.w3schools.com/bootstrap/bootstrap_filters.asp)
$(document).ready(function(){
    $(".searchInputs").on("keyup", function() {

        var value = $(this).val().toLowerCase();
        $(".commandTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
        
    });
});