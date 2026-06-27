
const AI = {

    async generate({

        endpoint,

        inputs = [],

        outputId,

        buttonId,

        statusId,

        responseKey = "result",

        successMessage = "Generated successfully.",

        loadingMessage = "Generating..."

    }) {

        const button = document.getElementById(buttonId);
        const output = document.getElementById(outputId);
        const status = document.getElementById(statusId);

        if (!button || !output || !status) {

            console.error("AI Utility: Required HTML elements not found.");

            return;
        }

        const payload = {};

        for (const input of inputs) {

            const element = document.getElementById(input.id);

            if (!element) {

                throw new Error(`Element '${input.id}' not found.`);

            }

            const value = element.value.trim();

            if (!value) {

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
            ${loadingMessage}
        `;

        status.innerHTML =
            "<span class='text-indigo-600'>Please wait...</span>";

        try {

            const response = await fetch(endpoint, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)

            });

            const data = await response.json();

            if (!response.ok) {

                throw new Error(
                    data.message || "AI generation failed."
                );

            }

            if (!(responseKey in data)) {

                throw new Error(
                    `Response key '${responseKey}' not found.`
                );

            }

            const generatedContent = data[responseKey];

            if (
                window.LMSCKEditor &&
                LMSCKEditor.editors &&
                LMSCKEditor.editors[outputId]
            ) {

                LMSCKEditor.editors[outputId].setData(generatedContent);

            }
            else {

                output.value = data[responseKey];
            }
            status.innerHTML =
                `<span class="text-green-600">✓ ${successMessage}</span>`;

        }

        catch (error) {

            console.error(error);

            status.innerHTML =
                `<span class="text-red-600">${error.message}</span>`;

        }

        finally {

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