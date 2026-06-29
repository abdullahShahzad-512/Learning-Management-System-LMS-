window.AI = {

    async generate({

        endpoint,
        inputs,
        outputId = null,
        buttonId,
        statusId,
        responseKey = "result",
        successMessage = "Generated successfully.",
        onSuccess = null

    }) 
    {

        const button = document.getElementById(buttonId);
        const status = document.getElementById(statusId);

        const output = outputId? document.getElementById(outputId): null;

        const payload = {};

        for (const input of inputs) 
        {

            const element = document.getElementById(input.id);

            if (!element) 
            {

                throw new Error(`Element '${input.id}' not found.`);

            }

            const value = element.value.trim();

            if (!value) 
            {

                status.innerHTML =
                    `<span class="text-red-600">${input.label} is required.</span>`;

                element.focus();

                return;

            }

            payload[input.key] = value;

        }

        button.disabled = true;

        button.innerHTML = `
            <span class="material-symbols-outlined animate-spin">
                progress_activity
            </span>
            Generating...
        `;

        status.innerHTML =
            "<span class='text-indigo-600'>Generating with AI...</span>";

        try 
        {

            const response = await fetch(endpoint, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)

            });

            const data = await response.json();

            if (!response.ok) 
            {

                throw new Error(data.message || "Generation failed.");

            }

            const result = data[responseKey];

            if (output && typeof result === "string") 
            {

                if (window.LMSCKEditor && LMSCKEditor.editors && LMSCKEditor.editors[outputId]) 
                {

                    LMSCKEditor.editors[outputId].setData(result);

                } 
                else 
                {

                    output.value = result;

                }

            }


            if (onSuccess) 
            {

                onSuccess(result);

            }

            status.innerHTML =
                `<span class="text-green-600">✓ ${successMessage}</span>`;

        }

        catch (error) 
        {

            console.error(error);

            status.innerHTML =
                `<span class="text-red-600">${error.message}</span>`;

        }

        finally 
        {

            button.disabled = false;

            button.innerHTML = `
                <span class="material-symbols-outlined">
                    auto_awesome
                </span>
                Generate with AI
            `;

        }

    }

};