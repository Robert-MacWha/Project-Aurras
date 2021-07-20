const fs = require('fs');

class Store {

    path = './_data/data.json';
    
    load() {

        //? load the data stored in the data json file

        // make sure the data file exists
        if (!fs.existsSync(this.path))
            this.reset();

        // load the json file containing all data
        let data = JSON.parse(fs.readFileSync(this.path));

        // parse the data into the individual parts and return them
        return { 
            entities: data.entities, intents: data.intents, prompts: data.prompts, global_id: data.global_id 
        };

    }

    save(entities, intents, prompts, global_id) {

        //? save the provided entities, intents, and prompts to the data.json file
        let data = {
            'entities': entities,
            'intents': intents,
            'prompts': prompts,
            'global_id': global_id
        }

        fs.writeFileSync(this.path, JSON.stringify(data));

    }

    reset() {

        //? reset / initialize the data.json file

        // create the template json structure
        let data = {
            'entities': {},
            'intents': {},
            'prompts': {},
            'global_id': 0
        }

        fs.writeFileSync(this.path, JSON.stringify(data));

    }
}

module.exports = Store;