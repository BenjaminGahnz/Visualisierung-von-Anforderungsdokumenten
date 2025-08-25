var sourceCodeController = (function() {    

    // Config parameters
    let controllerConfig = {
        fileType: "java",
        url: "",
        showCodeWindowButton: true,
        showCode: true,
    };

    function initialize(setupConfig) {
        application.transferConfigParams(setupConfig, controllerConfig);
    }

    function activate(rootDiv) {
        // Create HTML elements
        let codeViewDiv = document.createElement("DIV");
        codeViewDiv.id = "codeViewDiv";
        rootDiv.appendChild(codeViewDiv);

        if (controllerConfig.showCode === true) {
            // Code field
            let codeValueDiv = document.createElement("DIV");
            codeValueDiv.id = "codeValueDiv";
            let codePre = document.createElement("PRE");
            codePre.id = "codePre";
            codePre.style = "overflow:auto;";
            let codeTag = document.createElement("CODE");
            codeTag.id = "codeTag";

            codePre.appendChild(codeTag);
            codeValueDiv.appendChild(codePre);
            codeViewDiv.appendChild(codeValueDiv);
        }

        events.selected.on.subscribe(onEntitySelected);
    }

    function reset() {   
        const codeTag = $("#codeTag").get(0);    
        codeTag.textContent = "";
    }

    function onEntitySelected(applicationEvent) {
        const entity = applicationEvent.entities[0];
        // Only implementation for Requirements for now, later also for Famix.Namespace
        if (entity.type === "Namespace" && entity.belongsTo === "root") {
            // Package 
            reset();
            return;
        }
        displayCode(entity);          
    }

    function displayCode(entity) {
        const codeTag = $("#codeTag").get(0);
        getRequirement(entity).then(requirements => {
            // Clear the existing content
            codeTag.innerHTML = "";
    
            // Create a new element to display the entity name
            const entityNameElement = document.createElement("h2");
            entityNameElement.style.fontSize = "24px"; 
            entityNameElement.style.marginBottom = "16px"; 
            entityNameElement.textContent = entity.name;
    
            // Append the entity name element to the codeTag element
            codeTag.appendChild(entityNameElement);
    
            const table = document.createElement("table");
            table.style.width = "100%";
            table.style.borderCollapse = "collapse";
    
            for (const [key, value] of Object.entries(requirements)) {
                const row = document.createElement("tr");
    
                // Create a cell for the key
                const keyCell = document.createElement("td");
                keyCell.style.border = "1px solid #ddd";
                keyCell.style.padding = "8px";
                keyCell.innerHTML = `<strong>${key}</strong>`;
                row.appendChild(keyCell);
    
                // Create a cell for the value
                const valueCell = document.createElement("td");
                valueCell.style.border = "1px solid #ddd";
                valueCell.style.padding = "8px";
    
                // Check if the value contains XHTML
                if (isXHTML(value)) {
                    valueCell.innerHTML = value;
                } else {
                    valueCell.textContent = value;
                }
    
                row.appendChild(valueCell);
                table.appendChild(row);
            }
    
            // Append the table to the codeTag element
            codeTag.appendChild(table);
        });
    }
    

    async function getRequirement(entity) {
        const filePath = modelUrl + "/requirements.json";
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        
        
        // Navigate through the JSON structure to find the requirements for the given entity
        for (const document of data.documents) {
            for (const requirement of document.requirements) {
                if (requirement.id === entity.id) {
                    return requirement.content;
                }
            }
        }}

    function isXHTML(content) {
        // Simple check to see if the content contains XHTML tags
        const xhtmlPattern = /<\/?[a-z][\s\S]*>/i;
        return xhtmlPattern.test(content);
    }

    return {
        initialize: initialize,
        activate: activate,
        reset: reset,
    };
})();