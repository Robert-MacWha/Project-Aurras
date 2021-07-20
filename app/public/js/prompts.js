let intentID = Object.keys(intents)[0];

function reloadEntityTable() {
    // compile a table for the entities from the ejs template and render it
    window.api.ejs.renderFile('./public/html/partials/prompts-entity-table.ejs', { intent: intents[intentID], entities: entities }, function(err, str) {
        $('.entity-values').html(str);
    });
}

function reloadPromptTable() {
    // compile a table of the other prompts for this intent and render it
    let intentPrompts = [];
    for(const [key, value] of Object.entries(prompts)) { if (value.intent == intentID) { intentPrompts.push(value); } }

    window.api.ejs.renderFile('./public/html/partials/prompts-prompt-table.ejs', { prompts: intentPrompts, intents: intents, entities: entities }, function(err, str) {
        $('.prompt-table').html(str);
    });
}

$(function() {

    // if there was an intent stored, set the selected intent to that
    let prevIntentId = localStorage.getItem('intent');
    if (prevIntentId != null && prevIntentId in intents) { 
        
        intentID = prevIntentId;  
        $('.selectpicker').selectpicker('val', intentID);

        console.log($('select[name=intent]'));
    
    }

    reloadEntityTable();
    reloadPromptTable();

    // detect when a different intent is selected
    $('select').on('change', function(e) {

        intentID = this.value;

        reloadEntityTable();
        reloadPromptTable();

    });
    
});

// detect when the prompts form is submitted and store the current intent
$('form').submit(function(e) {

    localStorage.setItem('intent', intentID);

});